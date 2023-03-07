from controlcenter import Dashboard, widgets
from django.db.models import Count
from collections import defaultdict
from django.utils import timezone
import datetime
from .models import Customer, Order, Post, Comment, ShippingAddress
from django.contrib.auth.models import User


class OrderWeekSingleLineChart(widgets.SingleLineChart):
    limit_to = 7
    title = 'Commandes de Cette Semaine'
    model = Order
    width = widgets.LARGEST

    class Chartist:
            timestamp_options = {
            'year': 'numeric',
            'month': 'short',
            'day': 'short',
        }
            options = {
            'onlyInteger': True,
            'axisX': {
                'labelOffset': {
                    'x': -24,
                    'y': 0
                },
            },
            'chartPadding': {
                'top': 24,
                'right': 24,
            }
        }
        
    def labels(self):
        today = timezone.now().date()
        labels = [(today - datetime.timedelta(days=x)).strftime('%d/%m')
                  for x in range(self.limit_to)]
        return labels
        
    def series(self):
        series1 = []
        for label in self.labels:
            item = self.values[label]
            series1.append(item)
        series = []
        series.append(series1)
        return series
        
    # def legend(self):
    #     return [x for x in self.labels]

    def values(self):
        limit_to = self.limit_to * len(self.labels)
        queryset = self.get_queryset()
        queryset = queryset.extra({'order_day': 'order_day'}).values_list('order_day').annotate(count=Count('order_day')).order_by('-order_day')[:limit_to]
        values = defaultdict(lambda: 0)
        for order_day, count in queryset:
            order_day = order_day.strftime("%d-%m-%Y")
            day_month = '{0}/{1}'.format(*order_day.split('-'))
            values [day_month] = count
        return values


class OrderMonthSingleLineChart(widgets.SingleLineChart):
    limit_to = 30
    title = 'Commandes des Derniers 30 Jours'
    model = Order
    width = widgets.LARGEST

    class Chartist:
            timestamp_options = {
            'year': 'numeric',
            'month': 'short',
            'day': 'short',
        }
            options = {
            'onlyInteger': True,
            'axisX': {
                'labelOffset': {
                    'x': -24,
                    'y': 0
                },
            },
            'chartPadding': {
                'top': 24,
                'right': 24,
            }
        }
        
    def labels(self):
        today = timezone.now().date()
        labels = [(today - datetime.timedelta(days=x)).strftime('%d/%m')
                  for x in range(self.limit_to)]
        return labels
        
    def series(self):
        series1 = []
        for label in self.labels:
            item = self.values[label]
            series1.append(item)
        series = []
        series.append(series1)
        return series
        
    # def legend(self):
    #     return [x for x in self.labels]

    def values(self):
        limit_to = self.limit_to * len(self.labels)
        queryset = self.get_queryset()
        queryset = queryset.extra({'order_day': 'order_day'}).values_list('order_day').annotate(count=Count('order_day')).order_by('-order_day')[:limit_to]
        values = defaultdict(lambda: 0)
        for order_day, count in queryset:
            order_day = order_day.strftime("%d-%m-%Y")
            day_month = '{0}/{1}'.format(*order_day.split('-'))
            values [day_month] = count
        return values


class OrderYearSingleLineChart(widgets.SingleLineChart):
    limit_to = 12
    title = 'Commandes de Cette Année'
    model = Order
    width = widgets.LARGEST

    class Chartist:
            timestamp_options = {
            'year': 'numeric',
            'month': 'short',
            'day': 'short',
        }
            options = {
            'onlyInteger': True,
            'axisX': {
                'labelOffset': {
                    'x': -24,
                    'y': 0
                },
            },
            'chartPadding': {
                'top': 24,
                'right': 24,
            }
        }
        
    def labels(self):
        # today = timezone.now().date()
        # labels = [(today - datetime.timedelta(days=x)).strftime('%d/%m')
        #           for x in range(self.limit_to)]
        labels = ['Jan', 'Feb','Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return labels
        
    def series(self):
        series1 = []
        for label in self.labels:
            item = self.values[label]
            series1.append(item)
        series = []
        series.append(series1)
        return series
        
    # def legend(self):
    #     return [x for x in self.labels]

    def values(self):
        limit_to = self.limit_to * len(self.labels)
        queryset = self.get_queryset()
        queryset = queryset.extra({'order_day': 'order_day'}).values_list('order_day').annotate(count=Count('order_day')).order_by('-order_day')[:limit_to]
        values = defaultdict(lambda: 0)
        for order_day, count in queryset:
            order_day = order_day.strftime("%b")
            # day_month = '{0}/{1}'.format(*order_day.split('-'))
            values [order_day] = count
        return values

class PostPieChart(widgets.SinglePieChart):
    limit_to = 2
    title = 'Les Articles Les Plus Commentés'
    model = Comment 
    width = widgets.LARGE

    def labels(self):
        labels = []
        for serie in self.series:
            item = self.values[serie]
            labels.append(item)
        return labels

    def legend(self):
        legend= list(Post.objects.values_list('title', flat=True))
        return legend
        
    def series(self):
        series= list(Post.objects.values_list('id', flat=True))
        series = series
        return series

    def values(self):
        limit_to = self.limit_to * len(self.legend)
        queryset = self.get_queryset()
        queryset = queryset.extra({'post': 'post_id'}).values_list('post_id').alias(count=Count('post_id')).annotate(count=Count('post_id')).order_by('count')[:limit_to]
        values = defaultdict(lambda: 0)
        for post, count in queryset:
            values [post] = count
        return values

class UsersList(widgets.ItemList):
    # This widget displays a list of pizzas ordered today
    # in the restaurant
    title = 'Clients et Addresses'
    model = ShippingAddress 
    queryset = ShippingAddress.objects.all()
    list_display = ['customer','city', 'address']
    list_display_links = ['user']

    # By default ItemList limits queryset to 10 items, but we need all of them
    limit_to = 30

    # Sets widget's max-height to 300 px and makes it scrollable
    height = 300


                          
class MyDashboard(Dashboard):
    widgets = (
        PostPieChart,
        UsersList,
        OrderWeekSingleLineChart,
        OrderMonthSingleLineChart,
        OrderYearSingleLineChart,
    )

