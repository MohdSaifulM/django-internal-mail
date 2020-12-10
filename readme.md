# Django Internal Mailing System

## Description

<img src="https://i.pinimg.com/originals/56/c4/19/56c419f5a0989103beb622c8d794fffc.jpg" width="400" />

As a company we would like to have a way of sending secure mails to employees internally. Its a known fact that GMail, YahooMail and Hotmail aren't secure thus we are contracting our profound development team to handle this project. Just to let you know we had to let go of our random angmoh Chris to hire Jeff. Jeff feels we should make this a SPA(Single Page App) and has suggested making it with Django and using JavaScript to display the data to the HTML.

The app have already been setup for you. There are two apps in this django project, one for user `accounts` and the other for `mail`. You so you might what to have a look at all files and folders already setup to get familiar with the codes. The mail app consists of a javascript and css file and this is where most of your frontend code will go and a views.py where all your backend coding will reside.

Your task is to work in the `mail` app and completed the whole mailing system.

## Installation

1. Fork and clone the repository

### Pipenv installation
1. run `pipenv shell && pipenv install` to install all dependencies and set up virtual environment
1. run `pipenv run python manage.py makemigrations`
1. run `pipenv run python manage.py migrate`

or with just

### Pip installation
1. run `pip install -r requirement.txt` to install all dependencies
1. run `python manage.py makemigrations`
1. run `python manage.py migrate`
1. if you decide to use this way be sure to run `pip freeze > requirement.txt` after every new installation

## Deliverables

1. User should be able to compose email and send to registered email accounts in the app.
1. User should be able to send to more than one recipent seperated by `,`. i.e. `ebere@ga.co, siusing@ga.co, tristan@ga.co`
1. User Should be able to view mails in inbox without reloading the page. Real time changes arent needed.
1. User should be able to view sent items and archive mails.


## Screenshots Of possible design
<img src="https://www.getmailbird.com/wp-content/uploads/2020/08/Alternative-to-Mailbox-email-client.png" width="500" />

## Helper Code.

You can setup your serializers either with `django-restframework` by creating a `serializer.py` or writing custom serializers with your model.

<details><summary>With Django Rest Framework</summary>
<p>

```python
#serializers.py
class MailSerializer(serializers.ModelSerializer):
    class Meta:
      model = Mail
      fields = '__all__'
```

```python
#views.py
@api_view(['GET', 'PUT'])
 def mails_api(request, id):
      try:
        mail = Mail.objects.get(pk=id)
      except Mail.DoesNotExist:
        return JsonResponse({"message" : "Data not found"}, status=400)
      
      if request.method == 'PUT':
        serialize = MailSerializer(instance=mail, data=request.data)

        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        else:
            return Response(serialize.errors)
      
      serialize = MailSerializer(mail)
      return Response(serialize.data)
```
</p>
</details>

## Custom Serializer
Sometimes it is more beneficial to write your own serializers to handle api requests.

<details><summary>Custom Serializers with Model</summary>
<p>
You can also write your own serializer as so:

```python
#models.py
class Mail(models.Model):
  content = models.Text_Field()
  sender = models.ForeignKey(User, related_name="mails", on_delete=models.CASCADE)
  recipients = models.ManyToManyField("User", related_name="emails_received")
  subject = models.CharField(max_length=255)

  def serialize(self):
        return {
            "content": self.content,
            "sender": self.user.email,
            "subject" : self.subject,
            "recipients": [user.email for user in self.recipients.all()]
        }
```

```python
  #views.py
  from django.views.decorators.csrf import csrf_exempt

  @csrf_exempt
  def mails_api(request, id):
      try:
        mail = Mail.objects.get(pk=id)

        return JsonResponse(mail.serialize(), status=200)
      except Mail.DoesNotExist:
        return JsonResponse({"message" : "Data not found"}, status=400)

```
</p>
</details>
