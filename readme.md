# Django Internal Mailing System

## Description

<img src="https://www.lifewire.com/thmb/Jgby1eVME4lmPMnh6duppa9Q9r0=/1414x943/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/yandex-mail-10d3b62f5ac342ee956fa9cdc1a551b0.png" width="400" />

As a company we would like to have a way of mailing each other internally. Its a known fact that GMail, YahooMail and Hotmail have arent secure. We would also like to make this a SPA(Single Page App).

## Installation
1. Fork and clone the repository
1. run `pipenv shell && pipenv install` to install all dependencies and set up virtual environment

## Deliverables

1. User should be able to compose email and send to registered email accounts in the app.
1. User should be able to send to more than one recipent seperated by `,`. i.e. `ebere@ga.co, siusing@ga.co, tristan@ga.co`
1. User Should be able to view mails in inbox without reloading the page. Real time changes arent needed.
1. User should be able to view sent items and archive mails.




## Helper code.
You can setup your serializers either with `django-restframework` by creating a `serializer.py` and adding the following code to it.
```python
class MailSerializer(serializers.ModelSerializer):
    class Meta:
      model = Mail
      fields = '__all__'
```

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
