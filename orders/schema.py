from types import ClassMethodDescriptorType
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db import transaction

from shop.models.products import Product
from .models import Order, OrderItem


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ("id", "order", "product", "quantity")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "paid",
            "items",
        )


class OrderItemHelper:
    @classmethod
    def assign_ordered_items_to_order(cls, order, ordered_items):
        if ordered_items:
            for ordered_item in ordered_items:
                item = OrderItem(
                    order=order,
                    product=Product(pk=ordered_item.product_id),
                    quantity=ordered_item.quantity,
                )
                item.save()


class OrderHelper:
    @classmethod
    def assign_standard_fields(cls, order, order_input):
        standard_fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "paid",
        ]
        for key, value in order_input.items():
            if key in standard_fields:
                setattr(order, key, value)


class OrderItemInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
    quantity = graphene.Float(required=True)


class OrderCreateInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    address = graphene.String(required=True)
    city = graphene.String(required=True)
    ordered_items = graphene.List(OrderItemInput)


class CreateOrder(graphene.Mutation):
    class Arguments:
        order_input = OrderCreateInput()

    completed = graphene.Boolean()

    @staticmethod
    @transaction.atomic
    def mutate(root, info, order_input=None):
        order = Order()
        OrderHelper.assign_standard_fields(order=order, order_input=order_input)
        order.save()

        if order_input.ordered_items:
            OrderItemHelper.assign_ordered_items_to_order(
                order=order, ordered_items=order_input.ordered_items
            )

        order.save()

        return CreateOrder(completed=True)


class QueryOrder(graphene.ObjectType):
    order = graphene.Field(OrderType, order_id=graphene.ID(required=True))
    orders = graphene.List(OrderType)

    @staticmethod
    def resolve_order(_root, _info, order_id):
        return Order.objects.get(pk=order_id)

    @staticmethod
    def resolve_orders(_root, _info):
        return Order.objects.all()


class OrderMutation(graphene.ObjectType):
    create_order = CreateOrder().Field()
