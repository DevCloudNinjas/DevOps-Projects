import graphene
from graphene_django import DjangoObjectType
from .models import Transaction 

  
class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ("id", "date", "amount", "description", "type", "category", "account") 
        
          

class Query(graphene.ObjectType):
  """
  Queries for the Account model
  """
  transactions = graphene.List(TransactionType)

  def resolve_accounts(self, info, **kwargs):
    return Transaction.objects.all()


# class CreateAccount(graphene.Mutation):
#   class Arguments:
#     name = graphene.String()
#     initial_balance = graphene.Float()
#     active = graphene.Boolean()

#   ok = graphene.Boolean() 
#   account = graphene.Field(AccountType)

#   def mutate(self, info, name, initial_balance, active):
#     account = Account(name=name, initial_balance=initial_balance, active=active)
#     account.save()
#     return CreateAccount(ok=True, account=account)

# class DeleteAccount(graphene.Mutation):
#   class Arguments:
#     id = graphene.Int()

#   ok = graphene.Boolean()

#   def mutate(self, info, id):
#     account = Account.objects.get(id=id)
#     account.delete()
#     return DeleteAccount(ok=True)


# class UpdateAccount(graphene.Mutation):
#   class Arguments:
#     id = graphene.Int()
#     name = graphene.String()
#     initial_balance = graphene.Float()
#     active = graphene.Boolean()

#   ok = graphene.Boolean()
#   account = graphene.Field(AccountType)

#   def mutate(self, info, id, name, initial_balance, active):
#     account = Account.objects.get(id=id)
#     account.name = name
#     account.initial_balance = initial_balance
#     account.active = active
#     account.save()
#     return UpdateAccount(ok=True, account=account)


# class Mutation(graphene.ObjectType):
#   create_Account = CreateAccount.Field()
#   delete_Account = DeleteAccount.Field()
#   update_Account = UpdateAccount.Field()


schema = graphene.Schema(query=Query)