#~*~ coding: utf-8 ~*~
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def signup( request ):
    """Регистрация"""
    user = User()
    userProfile = UserProfile()
    if request.method == "POST":
        userForm = UserForm( request.POST, instance = user )
        userProfileForm = UserProfileForm( request.POST, instance = userProfile )
        if userForm.is_valid() and userProfileForm.is_valid():
            userData = userForm.cleaned_data
            user.username = userData['username']
            user.first_name = userData['firstname']
            user.last_name = userData['lastname']
            user.email = userData['email']
            user.set_password( userData['pass1'] )
            user.save()

            userProfile = user.get_profile()
            userProfileData = userProfileForm.cleaned_data
            userProfile.weight = userProfileData['weight']
            userProfile.save()
            user = authenticate( username = userData['username'], password = userData['pass1'] )
            login(request, user)
            return HttpResponseRedirect( "/accounts/profile/" )
    else:
        userForm = UserForm( instance = user )
        userProfileForm = UserProfileForm( instance = userProfile )
    return render_to_response( "accounts/signup.html", { "user_": user, "userProfile": userProfile, "userForm": userForm, "userProfileForm": userProfileForm }, context_instance = RequestContext( request ) )

@login_required
def profile( request ):
    """Профиль текущего пользователя"""
    user = request.user
    return render_to_response( "accounts/card.html", { "user": user }, context_instance = RequestContext( request ) )


@login_required
def user_card( request ):
    """Профиль текущего пользователя"""
    user = request.user
    return render_to_response( "accounts/card.html", { "user": user }, context_instance = RequestContext( request ) )
