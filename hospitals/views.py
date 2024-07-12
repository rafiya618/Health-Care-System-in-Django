from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,logout,login
from .models import *
from datetime import date
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
import stripe

#insert your stripe api key in it
stripe.api_key="YOUR SECRET KEY"


# Create your views here.


def Index(request):
    return render(request,'index.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['email']
        s = request.POST['subject']
        m = request.POST['message']
        try:
            Contact.objects.create(name=n, contact=c, email=e, subject=s, message=m, msgdate=date.today(), isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())


def adminlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_staff:
                login(request, user)
                error = "no"
                # Check if the user is in the 'Doctor' group
                if user.groups.filter(name='Doctor').exists():
                    return redirect('doctor_page')  # Redirect to the Doctor Page
                elif user.groups.filter(name='Reception').exists():
                    return redirect('reception')  # Redirect to the Reception Page
            else:
                error = "yes"
        else:
            error = "yes"
    return render(request, 'login.html', locals())

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    dc = Doctor.objects.all().count()
    pc = Patient.objects.all().count()
    ac = Appointment.objects.all().count()

    d = {'dc': dc, 'pc': pc, 'ac': ac}
    return render(request,'admin_home.html', d)

def Logout(request):
    logout(request)
    return redirect('index')

def add_doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    
    if request.method == 'POST':
        n = request.POST['name']
        m = request.POST['mobile']
        sp = request.POST['special']
        try:
            # Create Doctor object
            doctor = Doctor.objects.create(name=n, mobile=m, special=sp)
            
            # Create associated User object
            user = User.objects.create_user(username=m, password='defaultpassword')
            user.is_staff = True  # Set the user as staff
            user.save()
            
            # Assign Doctor object to User object
            doctor.user = user
            doctor.save()
            
            # Add user to the Doctor group
            doctor_group = Group.objects.get(name='Doctor')
            doctor_group.user_set.add(user)
            
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_doctor.html', locals())

def view_doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html', d)

def Delete_Doctor(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html', d)

def edit_doctor(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    doctor = Doctor.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        s1 = request.POST['special']

        doctor.name = n1
        doctor.mobile = m1
        doctor.special = s1

        try:
            doctor.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_doctor.html', locals())

def add_patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        g = request.POST['gender']
        m = request.POST['mobile']
        a = request.POST['address']
        s=request.POST['sickness']
        try:
            Patient.objects.create(name=n, gender=g, mobile=m, address=a,sickness=s)
            error = "no"
        except:
            error = "yes"
    return render(request,'add_patient.html', locals())

def view_patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat':pat}
    return render(request,'view_patient.html', d)

def Delete_Patient(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    pat = Patient.objects.all()
    d = {'pat':pat}
    return render(request,'view_patient.html', d)

def edit_patient(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    patient = Patient.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        g1 = request.POST['gender']
        a1 = request.POST['address']
        s1=request.POST['sickness']

        patient.name = n1
        patient.mobile = m1
        patient.gender = g1
        patient.address = a1
        patient.sickness=s1
        try:
            patient.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_patient.html', locals())

def add_appointment(request):
    error=""
    if not request.user.is_staff:
        return redirect('login')
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method=='POST':
        d = request.POST['doctor']
        p = request.POST['patient']
        d1 = request.POST['date']
        t = request.POST['time']
        doctor = Doctor.objects.filter(name=d).first()
        patient = Patient.objects.filter(name=p).first()
        try:
            Appointment.objects.create(doctor=doctor, patient=patient, date1=d1, time1=t)
            error="no"
        except:
            error="yes"
    d = {'doctor':doctor1,'patient':patient1,'error':error}
    return render(request,'add_appointment.html', d)

def view_appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.all()
    d = {'appointment':appointment}
    return render(request,'view_appointment.html', d)

def Delete_Appointment(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment1 = Appointment.objects.get(id=pid)
    appointment1.delete()
    appointment = Appointment.objects.all()
    d = {'appointment':appointment}
    return render(request,'view_appointment.html', d)

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

def add_reception(request):
    if not request.user.is_staff:
        return redirect('login')
    
    if request.method == 'POST':
        n = request.POST['name']
        m = request.POST['mobile']
        try:
            reception = Reception.objects.create(name=n, mobile=m)
            
            # Create associated User object
            user = User.objects.create_user(username=m, password='defaultpassword')
            user.is_staff = True  # Set the user as staff
            user.save()

            reception.user = user
            reception.save()

            reception_group = Group.objects.get(name='Reception')
            reception_group.user_set.add(user)
            
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_reception.html', locals())
def view_reception(request):
    if not request.user.is_staff:
        return redirect('login')
    rec = Reception.objects.all()
    d = {'rec':rec}
    return render(request,'view_reception.html', d)

def edit_reception(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    rec = Reception.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']

        rec.name = n1
        rec.mobile = m1


        try:
            rec.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_reception.html', locals())

def Reception_(request):
    if request.method == 'POST':
        if 'add_patient_form' in request.POST:
            # Handling adding a new patient
            name = request.POST['name']
            gender = request.POST['gender']
            mobile = request.POST['mobile']
            address = request.POST['address']
            try:
                Patient.objects.create(name=name, gender=gender, mobile=mobile, address=address)
                # Optionally, you can add a success message here
            except Exception as e:
                print(e)  # Handle the exception appropriately
            
        elif 'add_appointment_form' in request.POST:
            # Handling adding a new appointment
            doctor_id = request.POST['doctor']
            patient_id = request.POST['patient']
            date1 = request.POST['date']
            time1 = request.POST['time']
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                patient = Patient.objects.get(id=patient_id)
                Appointment.objects.create(doctor=doctor, patient=patient, date1=date1, time1=time1)
                # Optionally, you can add a success message here
            except Exception as e:
                print(e)  # Handle the exception appropriately

    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    appointments = Appointment.objects.all()
    return render(request, 'reception.html', {'doctors': doctors, 'patients': patients, 'appointments': appointments})

def Doctor_Page(request):
    if request.method == 'POST':
        if 'add_prescription_form' in request.POST:
            # Handling adding a new patient
            serial_number = request.POST['serial_number']
            doctor_id = request.POST['doctor']
            patient_id = request.POST['current_patient']
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                current_patient = Patient.objects.get(id=patient_id)
                Prescription.objects.create(serial_number=serial_number,doctor=doctor,current_patient=current_patient)
                # Optionally, you can add a success message here
            except Exception as e:
                print(e)  # Handle the exception appropriately
            
        elif 'add_report_form' in request.POST:
            # Handling adding a new patient
            report_number = request.POST['report_number']
            patient_id = request.POST['current_patient']
            try:
                current_patient = Patient.objects.get(id=patient_id)
                MedicalReport.objects.create(report_number=report_number,current_patient=current_patient)
                # Optionally, you can add a success message here
            except Exception as e:
                print(e)  # Handle the exception appropriately
        elif 'add_test_form' in request.POST:
            # Handling adding a new patient
            blood_group = request.POST['blood_group']
            patient_id = request.POST['current_patient']
            try:
                current_patient = Patient.objects.get(id=patient_id)
                Test.objects.create(blood_group=blood_group,current_patient=current_patient)
                # Optionally, you can add a success message here
            except Exception as e:
                print(e) 

    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    prescriptions=Prescription.objects.all()
    medical_reports=MedicalReport.objects.all()
    tests=Test.objects.all()
    return render(request, 'prescription_test_report.html', {'doctors': doctors, 'patients': patients, 'prescriptions': prescriptions,'medical_reports':medical_reports,'tests':tests})

def Doctor_Page_View(request):
    if not request.user.is_staff:
        return redirect('login')
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    prescriptions=Prescription.objects.all()
    medical_reports=MedicalReport.objects.all()
    tests=Test.objects.all()
    return render(request, 'viewOf_doctorPage_data.html', {'doctors': doctors, 'patients': patients, 'prescriptions': prescriptions,'medical_reports':medical_reports,'tests':tests})

def add_drug(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        p = request.POST['price']
        d = request.POST['exp_date']
        s=request.POST['stock']
        try:
            Drugs.objects.create(name=n,price=p,exp_date=d,stock=s)
            error = "no"
        except:
            error = "yes"
    return render(request,'add_drugs.html', locals())

def view_drug(request):
    drug = Drugs.objects.all()
    return render(request,'view_drugs.html', {'drug':drug})

def Delete_drug(request,pid):
    drug = Drugs.objects.get(id=pid)
    drug.delete()
    drug = Drugs.objects.all()
    return render(request,'view_drugs.html', {'drug':drug})

def edit_drug(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    drug = Drugs.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['name']
        p = request.POST['price']
        d = request.POST['exp_date']
        s=request.POST['stock']

        drug.name=n
        drug.price=p
        drug.exp_date=d
        drug.stock=s
        try:
            drug.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_drugs.html', locals())

def buy_drug(request, pid):
    # Get the drug object based on the drug_id
    drug = Drugs.objects.get(id=pid)
    
    # Check if the drug is in stock
    if drug.stock > 0:
        # Decrease the stock by one
        drug.stock -= 1
        drug.save()
        
        # Create a Bill entry for the purchased drug
        Bill.objects.create(amount=drug.price)  # Include the drug object in the Bill
        
        messages.success(request, f"{drug.name} purchased successfully!")
    else:
        messages.error(request, f"{drug.name} is out of stock!")

    d = Drugs.objects.all()
    
    # Redirect back to the drug list page
    return render(request, 'buy_page.html', {'d': d, 'purchased_drug': drug})  # Pass purchased drug info to the template

def buy_drug_view(request):
    d=Drugs.objects.all()
    
    # Redirect back to the drug list page
    return render(request,'buy_page.html',{'d':d})

def pay(request, pid):
    return render(request, 'charge.html', {'pid': pid})
def charge(request,pid):
    amount = pid
    if request.method == 'POST':
        print('Data:', request.POST)
        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['Fullname'],
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=500,
            currency='usd',
            description="Pay Bill"
        )

    return redirect(reverse('success', args=[amount]))



def successMsg(request, args):
	amount = args
	return render(request, 'success.html', {'amount':amount})
