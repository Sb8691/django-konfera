from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from konfera.models import (Receipt, Order, Location, Event, Sponsor, TicketType, DiscountCode, Ticket, Speaker, Talk,
                            Room, Schedule)


class SponsorshipInline(admin.TabularInline):
    model = Event.sponsors.through
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_from', 'date_to', 'event_type', 'status')
    list_filter = ('event_type', 'status')
    ordering = ('date_from', 'date_to', 'title')
    search_fields = ('=title',)
    readonly_fields = ('uuid', 'date_created', 'date_modified')
    fieldsets = (
        (_('Description'), {
            'fields': ('title', 'slug', 'description'),
        }),
        (_('Dates'), {
            'fields': ('date_from', 'date_to'),
        }),
        (_('Details'), {
            'fields': ('uuid', 'event_type', 'status', 'location', 'footer_text', 'analytics'),
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )
    inlines = [
        SponsorshipInline,
    ]
    prepopulated_fields = {
        'slug': ('title',),
    }

admin.site.register(Event, EventAdmin)


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'country', 'social_url',)
    list_filter = ('country', 'title', 'sponsor',)
    ordering = ('last_name', 'first_name',)
    search_fields = ('=last_name', '=first_name',)  # case insensitive searching
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        (_('Name'), {
            'fields': ('title', ('first_name', 'last_name',),)
        }),
        (_('Contact'), {
            'fields': ('email', 'phone',)
        }),
        (_('About'), {
            'fields': ('bio', 'country', ('url', 'social_url',), 'sponsor',)
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Speaker, SpeakerAdmin)


class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'primary_speaker', 'type', 'duration', 'event', 'status',)
    list_filter = ('type', 'duration', 'event', 'status',)
    search_fields = ('=title', '=primary_speaker__first_name', '=primary_speaker__last_name', '=event__title')
    ordering = ('title', 'event')
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        (_('Description'), {
            'fields': ('title', 'abstract', 'event',)
        }),
        (_('Details'), {
            'fields': (('type', 'duration',), 'status', ('primary_speaker', 'secondary_speaker',),)
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Talk, TalkAdmin)


class SponsoredEventsInline(admin.TabularInline):
    # Django 1.8 doesn't allow Sponsor.sponsored_events.through (caused by related_name)
    model = Event.sponsors.through
    verbose_name = _('Sponsored event')
    verbose_name_plural = _('Sponsored events')
    extra = 1


class SponsoredSpeakersInline(admin.StackedInline):
    model = Speaker
    verbose_name = _('Sponsored speaker')
    verbose_name_plural = _('Sponsored speakers')
    extra = 1


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'url',)
    list_filter = ('type',)
    search_fields = ('=title',)
    ordering = ('type', 'title',)
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        (_('Details'), {
            'fields': ('title', 'type', 'logo', 'url', 'about_us',)
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )
    inlines = [
        SponsoredEventsInline,
        SponsoredSpeakersInline,
    ]

admin.site.register(Sponsor, SponsorAdmin)


class RoomsInline(admin.StackedInline):
    model = Room
    extra = 1


class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'capacity')
    list_filter = ('city',)
    ordering = ('city', 'title')
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        (_('Details'), {
            'fields': ('title', 'capacity',)
        }),
        (_('Address'), {
            'fields': ('street', 'street2', 'state', 'city', 'postcode', 'get_here')
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )
    inlines = [
        RoomsInline,
    ]

admin.site.register(Location, LocationAdmin)


class ReceiptInline(admin.StackedInline):
    model = Receipt


class OrderAdmin(admin.ModelAdmin):
    list_display = ('purchase_date', 'price', 'discount', 'status', 'receipt_of')
    list_filter = ('status',)
    ordering = ('purchase_date',)
    search_fields = ('=uuid',)
    readonly_fields = ('purchase_date', 'payment_date', 'amount_paid', 'uuid', 'date_created', 'date_modified')
    fieldsets = (
        (_('Details'), {
            'fields': ('uuid', 'price', 'discount', 'status', 'amount_paid'),
        }),
        (_('Modifications'), {
            'fields': ('purchase_date', 'payment_date', 'date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )
    inlines = [
        ReceiptInline,
    ]

admin.site.register(Order, OrderAdmin)


class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'attendee_type', 'event', 'status')
    list_filter = ('attendee_type',)
    ordering = ('title', 'event')
    readonly_fields = ('status', 'uuid', 'date_created', 'date_modified')
    fieldsets = (
        (_('Details'), {
            'fields': ('title', 'description', 'uuid', 'price', 'attendee_type', 'event',)
        }),
        (_('Availability'), {
            'fields': ('date_from', 'date_to', 'status'),
            'classes': ('collapse',),
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(TicketType, TicketTypeAdmin)


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount', 'ticket_type', 'usage')
    ordering = ('title', 'ticket_type')
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        (_('Details'), {
            'fields': ('title', 'hash', 'ticket_type')
        }),
        (_('Discount'), {
            'fields': ('discount', 'usage')
        }),
        (_('Availability'), {
            'fields': ('date_from', 'date_to'),
            'classes': ('collapse',),
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(DiscountCode, DiscountCodeAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('email', 'type', 'status')
    list_filter = ('status', 'type__event',)
    ordering = ('order__purchase_date', 'email')
    search_fields = ('=last_name', '=first_name', '=email', )  # case insensitive searching
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        (_('Personal details'), {
            'fields': ('title', 'first_name', 'last_name', 'email', 'phone')
        }),
        (_('Ticket info'), {
            'fields': ('type', 'discount_code', 'status', 'description')
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Ticket, TicketAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('start', 'duration', 'talk', 'room')
    list_filter = ('talk__event', 'room')
    ordering = ('start', 'room', 'talk__event')
    search_fields = ('=description',)
    readonly_fields = ('date_created', 'date_modified')
    fieldsets = (
        (_('Time'), {
            'fields': ('start', 'duration'),
        }),
        (_('Details'), {
            'fields': ('talk', 'room', 'description')
        }),
        (_('Modifications'), {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Schedule, ScheduleAdmin)
