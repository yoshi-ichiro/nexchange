from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.template.loader import get_template

from core.common.views import DateFilterViewSet
from referrals.models import ReferralCode

from .models import Referral
from .permissions import IsLoggedIn
from .serializers import ReferralSerializer


class ReferralViewSet(DateFilterViewSet):
    serializer_class = ReferralSerializer
    premission_classes = (IsLoggedIn,)

    def get_queryset(self, *args, **kwargs):
        self.queryset = \
            Referral.objects.filter(code__user=self.request.user)
        return super(ReferralViewSet, self).get_queryset()


@login_required
def referrals(request):
    template = get_template('referrals/index_referrals.html')
    user = request.user
    referrals_code = ReferralCode.objects.filter(user=user).first()
    referrals_ = Referral.objects.filter(code=referrals_code)
    # return JsonResponse({'tests': referrals_[0].turnover})

    paginate_by = 10
    model = Referral
    kwargs = {"code": referrals_code}
    referrals_list = model.objects.filter(**kwargs)
    paginator = Paginator(referrals_list, paginate_by)
    page = request.GET.get('page')

    try:
        referrals_list = paginator.page(page)

    except PageNotAnInteger:
        referrals_list = paginator.page(1)

    except EmptyPage:
        referrals_list = paginator.page(paginator.num_pages)

    return HttpResponse(template.render({'referrals': referrals_,
                                         'referrals_list': referrals_list},
                                        request))
