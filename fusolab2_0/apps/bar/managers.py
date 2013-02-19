#from ingresso.managers import BalanceManager
from django.db import models
from datetime import datetime

class BalanceManager(models.Manager):

    def is_open(self,time=datetime.now):
        return super(BalanceManager, self).get_query_set().filter(Q(date__lt=time) & Q(operation__in=[Balance.OPENING,Balance.CLOSING])).latest('date').operation == Balance.OPENING

    def get_parent(self, time):
        return super(BalanceManager, self).get_query_set().filter(Q(operation=Balance.OPENING) & Q(date__lt=time)).latest('date')

    def get_closing_amount_before(self,current_opening):
        return super(BalanceManager, self).get_query_set().get(id=current_opening.id).get_previous_by_date(operation=Balance.CLOSING).amount

    def get_transactions_for(self, current_opening):
        return super(BalanceManager, self).get_query_set().filter(parent=current_opening)

    def get_opening_times(self,start_date,end_date):
        list = super(BalanceManager, self).get_query_set().filter(Q(date__range=[start_date,end_date]) & Q(parent__isnull=True)).select_related()
        ret = []
        for l in list:
            ret.append([l.date,BarBalance.objects.filter(Q(parent=l.id) & Q(operation=BarBalance.CLOSING)).get().date])
        return ret  

    def get_checkpoint_before(self,saved_balance):
        return super(BalanceManager, self).get_query_set().get(id=saved_balance.id).get_previous_by_date(operation=Balance.CASHPOINT)


class ReceiptManager(models.Manager):
	def total_between(self, opening_date, closing_date):
		if super(ReceiptManager, self).get_query_set().filter(date__range=[opening_date,closing_date]).exists():
			return super(ReceiptManager, self).get_query_set().filter(date__range=[opening_date,closing_date]).aggregate(Sum('total'))['total__sum']
		else:
			return Decimal('0.00')
	def receipts_between(self, opening_date, closing_date):
		return super(ReceiptManager, self).get_query_set().filter(date__range=[opening_date,closing_date])

