# The Python Imaging Library.
# $Id$

# Optional color management support, based on Kevin Cazabon's PyCMS
# library.

# History:

# 2009-03-08 fl   Added to PIL.

# Copyright (C) 2002-2003 Kevin Cazabon
# Copyright (c) 2009 by Fredrik Lundh
# Copyright (c) 2013 by Eric Soroos

# See the README file for information on usage and redistribution.  See
# below for the original description.

import sys

from PIL import Image

try:
    from PIL import _imagingcms
except ImportError as ex:
    # Allow error import for doc purposes, but error out when accessing
    # anything in core.
    from ._util import deferred_error

    _imagingcms = deferred_error(ex)

DESCRIPTION = """
pyCMS

    a Python / PIL interface to the littleCMS ICC Color Management System
    Copyright (C) 2002-2003 Kevin Cazabon
    kevin@cazabon.com
    http://www.cazabon.com

    pyCMS home page:  http://www.cazabon.com/pyCMS
    littleCMS home page:  http://www.littlecms.com
    (littleCMS is Copyright (C) 1998-2001 Marti Maria)

    Originally released under LGPL.  Graciously donated to PIL in
    March 2009, for distribution under the standard PIL license

    The pyCMS.py module provides a "clean" interface between Python/PIL and
    pyCMSdll, taking care of some of the more complex handling of the direct
    pyCMSdll functions, as well as error-checking and making sure that all
    relevant data is kept together.

    While it is possible to call pyCMSdll functions directly, it's not highly
    recommended.

    Version History:

        1.0.0 pil       Oct 2013 Port to LCMS 2.

        0.1.0 pil mod   March 10, 2009

                        Renamed display profile to proof profile. The proof
                        profile is the profile of the device that is being
                        simulated, not the profile of the device which is
                        actually used to display/print the final simulation
                        (that'd be the output profile) - also see LCMSAPI.txt
                        input colorspace -> using 'renderingIntent' -> proof
                        colorspace -> using 'proofRenderingIntent' -> output
                        colorspace

                        Added LCMS FLAGS support.
                        Added FLAGS["SOFTPROOFING"] as default flag for
                        buildProofTransform (otherwise the proof profile/intent
                        would be ignored).

        0.1.0 pil       March 2009 - added to PIL, as PIL.ImageCms

        0.0.2 alpha     Jan 6, 2002

                        Added try/except statements around type() checks of
                        potential CObjects... Python won't let you use type()
                        on them, and raises a TypeError (stupid, if you ask
                        me!)

                        Added buildProofTransformFromOpenProfiles() function.
                        Additional fixes in DLL, see DLL code for details.

        0.0.1 alpha     first public release, Dec. 26, 2002

    Known to-do list with current version (of Python interface, not pyCMSdll):

        none

"""

VERSION = "1.0.0 pil"

# --------------------------------------------------------------------.

core = _imagingcms

#
# intent/direction values

INTENT_PERCEPTUAL = 0
INTENT_RELATIVE_COLORIMETRIC = 1
INTENT_SATURATION = 2
INTENT_ABSOLUTE_COLORIMETRIC = 3

DIRECTION_INPUT = 0
DIRECTION_OUTPUT = 1
DIRECTION_PROOF = 2

#
# flags

FLAGS = {
    "MATRIXINPUT": 1,
    "MATRIXOUTPUT": 2,
    "MATRIXONLY": (1 | 2),
    "NOWHITEONWHITEFIXUP": 4,  # Don't hot fix scum dot
    # Don't create prelinearization tables on precalculated transforms
    # (internal use):
    "NOPRELINEARIZATION": 16,
    "GUESSDEVICECLASS": 32,  # Guess device class (for transform2devicelink)
    "NOTCACHE": 64,  # Inhibit 1-pixel cache
    "NOTPRECALC": 256,
    "NULLTRANSFORM": 512,  # Don't transform anyway
    "HIGHRESPRECALC": 1024,  # Use more memory to give better accuracy
    "LOWRESPRECALC": 2048,  # Use less memory to minimize resources
    "WHITEBLACKCOMPENSATION": 8192,
    "BLACKPOINTCOMPENSATION": 8192,
    "GAMUTCHECK": 4096,  # Out of Gamut alarm
    "SOFTPROOFING": 16384,  # Do softproofing
    "PRESERVEBLACK": 32768,  # Black preservation
    "NODEFAULTRESOURCEDEF": 16777216,  # CRD special
    "GRIDPOINTS": lambda n: ((n) & 0xFF) << 16,  # Gridpoints
}

_MAX_FLAG = 0
for flag in FLAGS.values():
    if isinstance(flag, int):
        _MAX_FLAG = _MAX_FLAG | flag


# --------------------------------------------------------------------.
# Experimental PIL-level API
# --------------------------------------------------------------------.

##
# Profile.


class ImageCmsProfile:
    def __init__(self, profile):
        """
        :param profile: Either a string representing a filename,
            a file like object containing a profile or a
            low-level profile object

        """

        if isinstance(profile, str):
            self._set(core.profile_open(profile), profile)
        elif hasattr(profile, "read"):
            self._set(core.profile_frombytes(profile.read()))
        elif isinstance(profile, _imagingcms.CmsProfile):
            self._set(profile)
        else:
            raise TypeError("Invalid type for Profile")

    def _set(self, profile, filename=None):
        self.profile = profile
        self.filename = filename
        if profile:
            self.product_name = None  # profile.product_name
            self.product_info = None  # profile.product_info
        else:
            self.product_name = None
            self.product_info = None

    def tobytes(self):
        """
        Returns the profile in a format suitable for embedding in
        saved images.

        :returns: a bytes object containing the ICC profile.
        """

        return core.profile_tobytes(self.profile)


class ImageCmsTransform(Image.ImagePointHandler):

    """
    Transform.  This can be used with the procedural API, or with the standard
    Image.point() method.

    Will return the output profile in the output.info['icc_profile'].
    """

    def __init__(
        self,
        input,
        output,
        input_mode,
        output_mode,
        intent=INTENT_PERCEPTUAL,
        proof=None,
        proof_intent=INTENT_ABSOLUTE_COLORIMETRIC,
        flags=0,
    ):
        if proof is None:
            self.transform = core.buildTransform(
                input.profile, output.profile, input_mode, output_mode, intent, flags
            )
        else:
            self.transform = core.buildProofTransform(
                input.profile,
                output.profile,
                proof.profile,
                input_mode,
                output_mode,
                intent,
                proof_intent,
                flags,
            )
        # Note: inputMode and outputMode are for pyCMS compatibility only
        self.input_mode = self.inputMode = input_mode
        self.output_mode = self.outputMode = output_mode

        self.output_profile = output

    def point(self, im):
        return self.apply(im)

    def apply(self, im, imOut=None):
        im.load()
        if imOut is None:
            imOut = Image.new(self.output_mode, im.size, None)
        self.transform.apply(im.im.id, imOut.im.id)
        imOut.info["icc_profile"] = self.output_profile.tobytes()
        return imOut

    def apply_in_place(self, im):
        im.load()
        if im.mode != self.output_mode:
            raise ValueError("mode mismatch")  # wrong output mode
        self.transform.apply(im.im.id, im.im.id)
        im.info["icc_profile"] = self.output_profile.tobytes()
        return im


def get_display_profile(handle=None):
    """ (experimental) Fetches the profile for the current display device.
    :returns: None if the profile is not known.
    """

    if sys.platform == "win32":
        from PIL import ImageWin

        if isinstance(handle, ImageWin.HDC):
            profile = core.get_display_profile_win32(handle, 1)
        else:
            profile = core.get_display_profile_win32(handle or 0)
    else:
        try:
            get = _imagingcms.get_display_profile
        except AttributeError:
            return None
        else:
            profile = get()
    return ImageCmsProfile(profile)


# --------------------------------------------------------------------.
# pyCMS compatible layer
# --------------------------------------------------------------------.


class PyCMSError(Exception):

    """ (pyCMS) Exception class.
    This is used for all errors in the pyCMS API. """

    pass


def profileToProfile(
    im,
    inputProfile,
    outputProfile,
    renderingIntent=INTENT_PERCEPTUAL,
    outputMode=None,
    inPlace=False,
    flags=0,
):
    """
    (pyCMS) Applies an ICC transformation to a given image, mapping from
    inputProfile to outputProfile.

    If the input or output profiles specified are not valid filenames, a"""
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponse
from django.http.response import JsonResponse
from .models import Registration
from django.contrib import auth
from django.contrib.auth import login,logout
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType
from product.models import Product
from django.contrib.sites.models import Site
from product.models import Seller
from datetime import datetime
from django.shortcuts import get_object_or_404
def signup(request):
    #cookies
    if "user_id" in request.COOKIES:
        uid = request.COOKIES["user_id"]
        user = get_object_or_404(User, id=uid)
        auth.login(request, user)
        if user.is_superuser:
            return HttpResponseRedirect("/admin")
        elif user.is_staff:
            return HttpResponseRedirect('../sellerdashboard')
        else:
            return HttpResponseRedirect('../customerdashboard')

    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        user_name=request.POST['user_name']
        mobile=request.POST['mobile']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        user_type=request.POST['user_type']
        msg='your account has been created successfully'
        subject='Account created'
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return render(request,'Accounts/signup..html')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,email=email,password=password)
                user.save()
                auth.login(request, user)
                messages.success(request, 'Account created succesfully')
                if user_type=="sell":
                    user.is_staff=True
                    seller=Seller(user=user,mobile_number=mobile)
                    seller.save()
                else:
                    reg = Registration(user=user,mobile_number=mobile)
                    reg.save()

                user=auth.authenticate(request,username=user_name,password=password)
                if user:
                    try:
                        em=EmailMessage(subject,msg,to=[user.email])
                        em.send()
                        messages.success(request,'email sent successfully')
                    except:
                        messages.error(request,'could not send')

                    if user.is_staff:
                        return redirect('sellerdashboard')
                    else:
                        return redirect('custdashboard')
                else:
                    messages.error(request,'fill credentials')

        else:
            messages.error(request,'Password did not match')
            return render(request,'Accounts/signup.html')
    else:
        return render(request,'Accounts/signup.html')
def check_user(request):
    if request.method=='GET':
        email=request.GET['email']
        if User.objects.filter(email=email).exists():
            return HttpResponse('Email already taken')
        else:
            return HttpResponse('Doesnot exists')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        Password=request.POST['Password']
        user=auth.authenticate(username=username,password=Password)
        if user:
            auth.login(request,user)
            if user.is_superuser:
                messages.success(request, 'You have  logged in through site')
                return HttpResponseRedirect('/admin')
            elif user.is_staff:
                messages.success(request,'You are logged in')
                res= HttpResponseRedirect('../sellerdashboard')
                if "rememberme" in request.POST:
                    res.set_cookie('user_id',user.id)
                    res.set_cookie('date_login',datetime.now())
                return res
            else:
                messages.success(request, 'You are logged in')
                res = HttpResponseRedirect('../customerdashboard')
                if "rememberme" in request.POST:
                    res.set_cookie('user_id', user.id)
                    res.set_cookie('date_login', datetime.now())
                return res

        else:
            messages.error(request,'Fill credentials properly')
            return render(request,'Accounts/login.html')
    else:
        return render(request,'Accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out')
    #cookies
    res = HttpResponseRedirect("/")
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    return res
def custdashboard(request):
    data=Registration.objects.get(user__id=request.user.id)
    context={'data':data}
    return render(request,'Accounts/custdashboard.html',context)
def sellerdashboard(request):
    data =Seller.objects.get(user__id=request.user.id)
    context = {'data': data}
    return render(request, 'Accounts/sellerdashboard.html',context)
def changepass(request):
    if request.method=='POST':
        username=request.POST['username']
        oldpass= request.POST['oldpass']
        newpass = request.POST['newpass']
        cnfrmpass=request.POST['cnfrmpass']
        if newpass==cnfrmpass:
            user=User.objects.get(id=request.user.id)
            username=user.username
            match=user.check_password(oldpass)
            if match:
                user.set_password(newpass)
                user.save()
                user=User.objects.get(username=username)
                auth.login(request,user)
                messages.success(request,'Password changed successfully')
                msg = 'your account has been created successfully'
                subject = 'Account created'
                try:
                    em=EmailMessage(msg,subject,to=[user.email])
                    em.send()
                    messages.success(request, 'email sent successfully')
                except:
                    messages.error(request, 'could not send')

                if user.is_staff:
                    return redirect('sellerdashboard')
                else:
                    return redirect('custdashboard')
            else:
                messages.error(request,'please check old password')
                return render(request,'Accounts/changepass.html')
        else:
            messages.error(request,'newpassword didnt match')
            return render(request,'Accounts/changepass.html')
    else:
        return render(request, 'Accounts/changepass.html')



def customer_edit_profile(request):
    context={}
    check=Registration.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data=Registration.objects.get(user__id=request.user.id)
        context['data']=data
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        city = request.POST['city']
        contact = request.POST['contact']
        gender=request.POST['gender']
        age=request.POST['age']
        user=User.objects.get(id=request.user.id)
        user.first_name=fname
        user.last_name=lname
        user.email=email
        user.save()

        data.city=city
        data.gender=gender
        data.mobile_number=contact
        data.age=age
        data.save()

        if 'image' in request.FILES:
            img=request.FILES['image']
            data.image=img
            data.save()
        messages.success(request,'profile updated')
        return render(request,'Accounts/customer_edit_profile.html',context)
    else:
        return render(request,'Accounts/customer_edit_profile.html',context)
def seller_edit_profile(request):
    context = {}
    check = Seller.objects.filter(user__id=request.user.id)
    if len(check) > 0:
        data =Seller.objects.get(user__id=request.user.id)
        context['data'] = data
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        city = request.POST['city']
        contact = request.POST['contact']
        gender = request.POST['gender']
        age = request.POST['age']
        shop_name=request.POST['shop_name']
        aadhar_card_no=request.POST['aadhar_card_no']
        shop_GST_no=request.POST['shop_GST_no']
        user = User.objects.get(id=request.user.id)
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.save()

        data.city = city
        data.gender = gender
        data.mobile_number = contact
        data.age = age
        data.aadhar_card_no=aadhar_card_no
        data.shop_GST_no=shop_GST_no
        data.shop_name=shop_name
        data.save()

        if 'image' in request.FILES:
            img = request.FILES['image']
            data.image = img
            data.save()
        if 'aadhar_pic' in request.FILES:
            aadhar_pic=request.FILES['aadhar_pic']
            data.aadhar_pic=aadhar_pic
            data.save()
        messages.success(request, 'profile updated')
        return render(request, 'Accounts/seller_edit_profile.html', context)
    else:
        return render(request, 'Accounts/seller_edit_profile.html', context)

def adminprofile(request):
    return render(request,'Accounts/adminprofile.html')
