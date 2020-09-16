from django.contrib import admin
from analytics.models import ViewPollItemsUnique, ViewPollTypeUnique, Ranking, ScorePollItemsByMonth, ScoreUserByMonth, PostReport
from analytics.models import PromoAnalytic, MarketingPromo, ControlTable


class ViewPollItemsUniqueAdmin(admin.ModelAdmin):
    list_display = ('p_item', 'vcount', 'updated', 'timestamp')

    def __str__(self,obj):
        return obj.__str__()

class ViewPollTypeUniqueAdmin(admin.ModelAdmin):
    list_display = ('p_type', 'id', 'vcount', 'ecount', 'updated', 'timestamp')

    def __str__(self,obj):
        return obj.__str__()
        
class RankingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'low_score', 'high_score', 'add_days')


class ScorePollItemsByMonthAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'year', 'month', 'posi', 'nega', 'score', 'updated')

class ScoreUserByMonthAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'year', 'month', 'score', 'updated')

class PostReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'Puser', 'usercon', 'postissue','postissuemsg', 'timestamp')





# Register your models here.
class PromoAnalyticAdmin(admin.ModelAdmin):
    # list_display = ('id','referrer', 'referred', 'date','active', 'ref_id')
    list_display = ('id','promoname','promotype','referrer', 'promouser', 'date', 'ref_id')
    search_fields = ['promoname']
    # list_filter = ('active', 'freepoll','locked')

    def __str__(self, obj):
        return obj.__str__()

# Register your models here.
class MarketingPromoAdmin(admin.ModelAdmin):
    # list_display = ('id','referrer', 'referred', 'date','active', 'ref_id')
    list_display = ('id','promoname','promotype','referrer', 'date', 'active', 'promoid')
    search_fields = ['promoname']
    list_filter = ('active','promotype')

    def __str__(self, obj):
        return obj.__str__()



# Register your models here.
class ControlTableAdmin(admin.ModelAdmin):
    # list_display = ('id','referrer', 'referred', 'date','active', 'ref_id')
    list_display = ('id','controlname','postadddelay','signupdays', 'removepostdvotes', 'freedaysreferral', 'notiweekday', 'notihour', 'notiminute', 'delaypopsurvey')
    # search_fields = ['title']
    # list_filter = ('active', 'freepoll','locked')

    def __str__(self, obj):
        return obj.__str__()


admin.site.register(ViewPollItemsUnique, ViewPollItemsUniqueAdmin)
admin.site.register(ViewPollTypeUnique, ViewPollTypeUniqueAdmin)
admin.site.register(Ranking, RankingAdmin)
admin.site.register(ScorePollItemsByMonth, ScorePollItemsByMonthAdmin)
admin.site.register(ScoreUserByMonth, ScoreUserByMonthAdmin)
admin.site.register(PostReport, PostReportAdmin)
admin.site.register(ControlTable, ControlTableAdmin)
admin.site.register(MarketingPromo, MarketingPromoAdmin)
admin.site.register(PromoAnalytic, PromoAnalyticAdmin)