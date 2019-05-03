from django import forms
from django.core.exceptions import ValidationError
from django.db import connection

from .models import Item, Vendor, CurrentEvent
## The following would result in circular import; do it manually or move function to special helper file.
#from baskets.views import get_current_event

class VendorForm(forms.ModelForm):

  class Meta:
    model = Vendor
    fields = ('first_name', 'last_name', 'vendor_number', 'address', 'phone', 'events')
#    widgets = {
#        'vendorID': forms.NumberInput(), 
#        #'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#        }


class AddItemForm(forms.Form):
  vendor = forms.IntegerField(min_value=1, max_value = 200, required=True, label="Verkäufer")
  price = forms.DecimalField(min_value=0, max_value= 1000, decimal_places=2, required=True, label="Preis")

  def clean_vendor(self):
    current_event = CurrentEvent.objects.latest('last_touched').event_id 
    current_event_id = current_event.id 
    assert isinstance(current_event_id, int)
    with connection.cursor() as cursor:
      cursor.execute('''SELECT bv.vendor_number AS vn
                        FROM baskets_vendor_events AS bve
                        JOIN baskets_vendor AS bv 
                          ON bv.id=bve.vendor_id
                        WHERE event_id=%s 
                        GROUP BY vn
                        ORDER BY vn''',(current_event_id,))
      _allowed_vendors = [vid[0] for vid in cursor.fetchall()]
    ## This one simply checks if vendor exists:
    #_allowed_vendors = Vendor.objects.values_list('vendor_number', flat=True)
    if not self.cleaned_data.get('vendor') in _allowed_vendors:
      raise ValidationError("Verkäufer existiert nicht.")  #.format(_allowed_vendors))
    return self.cleaned_data


#
#
#class GiveCreditForm(forms.ModelForm):
#  
#  def __init__(self, *args, **kwargs):
#    max_values = kwargs.pop('max_values', None)
#    user = kwargs.pop('user', None)
#    config = kwargs.pop('config', None)
#    super(GiveCreditForm, self).__init__(*args, **kwargs)
#    if max_values:
#      self.fields['credits'] = forms.DecimalField(min_value=0, max_value=max_values['credits'])
#      self.fields['credits'].help_text = 'max. {} credits'.format(max_values['credits'])
#      if not config['bonus_credits']:
#        ## if we do not want to use bonus_credits, hide this input 
#        self.fields['bonus_credits'].widget = forms.HiddenInput()
#      else:
#        self.fields['bonus_credits'] = forms.DecimalField(min_value=0, max_value=max_values['bonus_credits'])
#        self.fields['bonus_credits'].help_text = 'max. {} bonus_credits'.format(max_values['bonus_credits'])
#    if 'instance' in kwargs and kwargs['instance']:
#      ## in this case we have selected a student and an exercise before, so fix both:

#      _students = Student.objects.filter(id=kwargs['instance'].student.id)
#      _exercise = Exercise.objects.filter(id=kwargs['instance'].exercise.id)
#      self.fields['student'].queryset = _students
#      self.fields['student'].initial = _students
#      self.fields['exercise'].queryset = _exercise
#      self.fields['exercise'].initial = _exercise
#    else:
#      if user:
#        _students = Student.objects.select_related('exgroup__tutor').filter(exgroup__tutor=user)
#        self.fields['student'].queryset = _students
#        self.fields['student'].initial = _students
#
#
#  class Meta:
#    model = Result
#    fields = ('student', 'exercise', 'credits', 'bonus_credits', 'blackboard', )
#
#
#
#
#class AssignPresenceForm(forms.ModelForm):
#
#  def __init__(self, *args, **kwargs):
#    user = kwargs.pop('user', None)
#    super(AssignPresenceForm, self).__init__(*args, **kwargs)
#    if 'instance' in kwargs and kwargs['instance']:
#      ## in this case we selected a student and exercise sheet -> fix them in the form
#      _students = Student.objects.filter(id=kwargs['instance'].student.id)
#      _sheet = Sheet.objects.filter(id=kwargs['instance'].sheet.id)
#      self.fields['student'].queryset = _students
#      self.fields['student'].initial = _students
#      self.fields['sheet'].queryset = _sheet
#      self.fields['sheet'].initial = _sheet
#
#    else:
#      if user:
#        _students = Student.objects.select_related('exgroup__tutor').filter(exgroup__tutor=user)
#        self.fields['student'].queryset = _students
#        self.fields['student'].initial = _students
#
#  class Meta:
#    model = Presence
#    fields = ('student', 'sheet', 'present')
#
#
#
#
#
#class EditStudentForm(forms.ModelForm):
#
#  def __init__(self, *args, **kwargs):
#    user = kwargs.pop('user', None)
#    super(EditStudentForm, self).__init__(*args, **kwargs)
##    if 'instance' in kwargs and kwargs['instance']:
##      ## in this case we selected a student and exercise sheet -> fix them in the form
##      _students = Student.objects.filter(id=kwargs['instance'].student.id)
##      _sheet = Sheet.objects.filter(id=kwargs['instance'].sheet.id)
##      self.fields['student'].queryset = _students
##      self.fields['student'].initial = _students
##      self.fields['sheet'].queryset = _sheet
##      self.fields['sheet'].initial = _sheet
##
##    else:
##      if user:
##        _students = Student.objects.select_related('exgroup__tutor').filter(exgroup__tutor=user)
##        self.fields['student'].queryset = _students
##        self.fields['student'].initial = _students
#
#  class Meta:
#    model = Student
#    fields = ('email', )
