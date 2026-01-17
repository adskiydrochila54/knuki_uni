from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
import json

from .models import ContactMessage, ContactFormConfig


class LocalizedJSONWidget(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {
            'rows': 4,
            'style': 'width: 100%; font-family: monospace; font-size: 13px;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value:
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    pass
            if isinstance(value, (dict, list)):
                return json.dumps(value, ensure_ascii=False, indent=2)
        return super().format_value(value)


class ContactFormConfigForm(forms.ModelForm):
    class Meta:
        model = ContactFormConfig
        fields = '__all__'
        widgets = {
            'form_title': LocalizedJSONWidget(),
            'form_description': LocalizedJSONWidget(),
            'label_name': LocalizedJSONWidget(),
            'label_faculty': LocalizedJSONWidget(),
            'label_phone': LocalizedJSONWidget(),
            'label_message': LocalizedJSONWidget(),
            'placeholder_name': LocalizedJSONWidget(),
            'placeholder_faculty': LocalizedJSONWidget(),
            'placeholder_phone': LocalizedJSONWidget(),
            'placeholder_message': LocalizedJSONWidget(),
            'faculty_options': LocalizedJSONWidget(),
            'submit_button_text': LocalizedJSONWidget(),
            'success_message': LocalizedJSONWidget(),
            'error_message': LocalizedJSONWidget(),
            'validation_name_min_length': LocalizedJSONWidget(),
            'validation_message_min_length': LocalizedJSONWidget(),
            'validation_phone_invalid': LocalizedJSONWidget(),
            'validation_faculty_required': LocalizedJSONWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()

        json_fields = [
            'form_title', 'form_description',
            'label_name', 'label_faculty', 'label_phone', 'label_message',
            'placeholder_name', 'placeholder_faculty', 'placeholder_phone', 'placeholder_message',
            'submit_button_text', 'success_message', 'error_message',
            'validation_name_min_length', 'validation_message_min_length',
            'validation_phone_invalid', 'validation_faculty_required',
        ]

        required_languages = {'ky', 'ru', 'en'}

        for field_name in json_fields:
            value = cleaned_data.get(field_name)

            if not value:
                continue
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                    cleaned_data[field_name] = value
                except json.JSONDecodeError as e:
                    raise forms.ValidationError({
                        field_name: f'Некорректный JSON: {str(e)}'
                    })
            if not isinstance(value, dict):
                raise forms.ValidationError({
                    field_name: 'Значение должно быть JSON-объектом'
                })
            missing_languages = required_languages - set(value.keys())
            if missing_languages:
                raise forms.ValidationError({
                    field_name: f'Отсутствуют переводы для языков: {", ".join(missing_languages)}'
                })
            for lang, text in value.items():
                if not isinstance(text, str) or not text.strip():
                    raise forms.ValidationError({
                        field_name: f'Перевод для языка "{lang}" не может быть пустым'
                    })

        faculty_options = cleaned_data.get('faculty_options')
        if faculty_options:
            if isinstance(faculty_options, str):
                try:
                    faculty_options = json.loads(faculty_options)
                    cleaned_data['faculty_options'] = faculty_options
                except json.JSONDecodeError as e:
                    raise forms.ValidationError({
                        'faculty_options': f'Некорректный JSON: {str(e)}'
                    })

            if not isinstance(faculty_options, list):
                raise forms.ValidationError({
                    'faculty_options': 'Должен быть массив объектов'
                })

            for idx, item in enumerate(faculty_options):
                if not isinstance(item, dict):
                    raise forms.ValidationError({
                        'faculty_options': f'Элемент {idx} должен быть объектом'
                    })
                if 'value' not in item or 'label' not in item:
                    raise forms.ValidationError({
                        'faculty_options': f'Элемент {idx} должен содержать "value" и "label"'
                    })
                if not isinstance(item['label'], dict):
                    raise forms.ValidationError({
                        'faculty_options': f'Элемент {idx}: "label" должен быть объектом с переводами'
                    })
                missing = required_languages - set(item['label'].keys())
                if missing:
                    raise forms.ValidationError({
                        'faculty_options': f'Элемент {idx}: отсутствуют переводы {", ".join(missing)}'
                    })

        return cleaned_data


@admin.register(ContactFormConfig)
class ContactFormConfigAdmin(admin.ModelAdmin):
    form = ContactFormConfigForm

    fieldsets = (
        ('🎯 Основные тексты формы', {
            'fields': ('form_title', 'form_description'),
            'description': 'Заголовок и описание формы обратной связи'
        }),
        ('🏷️ Labels полей формы', {
            'fields': ('label_name', 'label_faculty', 'label_phone', 'label_message'),
            'classes': ('collapse',),
        }),
        ('💬 Placeholders', {
            'fields': ('placeholder_name', 'placeholder_faculty', 'placeholder_phone', 'placeholder_message'),
            'classes': ('collapse',),
        }),
        ('🎓 Факультеты', {
            'fields': ('faculty_options',),
            'description': 'Формат: [{"value": "faculty1", "label": {"ky": "...", "ru": "...", "en": "..."}}]'
        }),
        ('🔘 Кнопки и сообщения', {
            'fields': ('submit_button_text', 'success_message', 'error_message'),
        }),
        ('⚠️ Сообщения валидации', {
            'fields': ('validation_name_min_length', 'validation_message_min_length',
                       'validation_phone_invalid', 'validation_faculty_required'),
            'classes': ('collapse',),
        }),
        ('📅 Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return not ContactFormConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class ContactMessageStatusFilter(admin.SimpleListFilter):
    title = 'Статус'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('unread', 'Непрочитанные'),
            ('read', 'Прочитанные'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'unread':
            return queryset.filter(is_read=False)
        if self.value() == 'read':
            return queryset.filter(is_read=True)
        return queryset


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name_with_status',
        'faculty_display',
        'phone_display',
        'created_at_display',
        'status_badge',
    )

    list_filter = (
        ContactMessageStatusFilter,
        'created_at',
        'faculty',
    )

    search_fields = (
        'name',
        'phone',
        'faculty',
        'message',
    )

    readonly_fields = (
        'name',
        'faculty',
        'phone',
        'message',
        'created_at',
        'message_preview',
    )

    fieldsets = (
        ('👤 Контактная информация', {
            'fields': ('name', 'faculty', 'phone'),
        }),
        ('📨 Сообщение', {
            'fields': ('message_preview',),
        }),
        ('📊 Метаданные', {
            'fields': ('created_at', 'is_read'),
        }),
    )

    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25

    actions = [
        'mark_as_read',
        'mark_as_unread',
        'export_to_csv',
    ]

    @admin.display(description='Имя', ordering='name')
    def name_with_status(self, obj):
        if not obj.is_read:
            return format_html('<strong>🔴 {}</strong>', obj.name)
        return obj.name

    @admin.display(description='Факультет', ordering='faculty')
    def faculty_display(self, obj):
        return obj.faculty

    @admin.display(description='Телефон', ordering='phone')
    def phone_display(self, obj):
        return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)

    @admin.display(description='Дата', ordering='created_at')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

    @admin.display(description='Статус')
    def status_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-size: 11px; font-weight: bold;">✓ Прочитано</span>'
            )
        return format_html(
            '<span style="background: #dc3545; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">● Новое</span>'
        )

    @admin.display(description='Сообщение')
    def message_preview(self, obj):
        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 5px; '
            'border-left: 4px solid #417690; white-space: pre-wrap; '
            'font-family: system-ui, -apple-system, sans-serif; line-height: 1.6;">{}</div>',
            obj.message
        )

    @admin.action(description='✓ Отметить как прочитанное')
    def mark_as_read(self, request, queryset):
        updated = queryset.filter(is_read=False).update(is_read=True)
        self.message_user(request, f'Отмечено как прочитанное: {updated} сообщений')

    @admin.action(description='○ Отметить как непрочитанное')
    def mark_as_unread(self, request, queryset):
        updated = queryset.filter(is_read=True).update(is_read=False)
        self.message_user(request, f'Отмечено как непрочитанное: {updated} сообщений')

    @admin.action(description='📥 Экспорт в CSV')
    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from datetime import datetime

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response[
            'Content-Disposition'] = f'attachment; filename="contact_messages_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        response.write('\ufeff')

        writer = csv.writer(response)
        writer.writerow(['ID', 'Имя', 'Факультет', 'Телефон', 'Сообщение', 'Дата создания', 'Прочитано'])

        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.name,
                obj.faculty,
                obj.phone,
                obj.message,
                obj.created_at.strftime('%d.%m.%Y %H:%M:%S'),
                'Да' if obj.is_read else 'Нет',
            ])

        return response

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return super().get_readonly_fields(request, obj)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        total = ContactMessage.objects.count()
        unread = ContactMessage.objects.filter(is_read=False).count()
        read = ContactMessage.objects.filter(is_read=True).count()

        extra_context['total_messages'] = total
        extra_context['unread_messages'] = unread
        extra_context['read_messages'] = read
        extra_context['unread_percentage'] = round((unread / total * 100) if total > 0 else 0, 1)

        return super().changelist_view(request, extra_context)


admin.site.site_header = "Управление формой обратной связи"
admin.site.site_title = "Contact Admin"
admin.site.index_title = "Добро пожаловать в панель управления"