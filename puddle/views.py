from .forms import SignupForm, ChatLinkFormSet, NewsletterForm, RemoveChatForm
from django.contrib.auth import logout
from asgiref.sync import async_to_sync
from .models import Groups, Newsletter
from .telegram_client import request_telegram_code, complete_telegram_auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import threading
import asyncio
from .telegram_service import send_newsletter_for_user_data, log_store


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'puddle/signup.html', {'form': form})


def logout_v(request):
    logout(request)
    return redirect('/login/')


def home_page(request):
    user = request.user
    return render(request, 'puddle/home_page.html', context={'user': user})


@login_required
def send_telegram_code_view(request):
    if request.method == 'POST':
        user = request.user
        session_string, phone_code_hash = async_to_sync(request_telegram_code)(user)
        request.session['telegram_temp_session'] = session_string
        request.session['telegram_code_hash'] = phone_code_hash
        return redirect('/telegram/confirm-code/')
    return render(request, 'puddle/request_code.html')


@login_required
def confirm_telegram_code_view(request):
    if request.method == 'POST':
        user = request.user
        code = request.POST.get('code')
        password = request.POST.get('password') or None

        session_string = request.session.get('telegram_temp_session')
        phone_code_hash = request.session.get('telegram_code_hash')

        if not session_string or not phone_code_hash:
            return JsonResponse({"error": "Сначала отправьте код."}, status=400)

        try:
            async_to_sync(complete_telegram_auth)(user, session_string, code, phone_code_hash, password)
            return redirect('/')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, 'puddle/confirm_code.html')


@login_required()
def add_chats(request):
    if request.method == 'POST':
        formset = ChatLinkFormSet(request.POST, prefix='chats')
        if formset.is_valid():
            links = [form.cleaned_data['link']
                     for form in formset
                     if form.cleaned_data.get('link')]

            group, created = Groups.objects.get_or_create(
                user=request.user,
                defaults={'chats': []}
            )

            added = group.add_chats(links)

            if added > 0:
                return redirect('/')
            else:
                for form in formset:
                    if form.cleaned_data.get('link') in group.get_chats():
                        form.add_error('link', 'Эта ссылка уже была добавлена ранее')
    else:
        formset = ChatLinkFormSet(prefix='chats')

    return render(request, 'puddle/add.html', {
        'formset': formset,
        'title': 'Добавление чатов'
    })


@login_required
def list_chats(request):
    groups = Groups.objects.get(user=request.user)
    chats = groups.get_chats()

    if request.method == 'POST':
        form = RemoveChatForm(request.POST)
        if form.is_valid():
            chat_url = form.cleaned_data['chat_url']
            if chat_url in chats:
                chats.remove(chat_url)
                groups.chats = chats
                groups.save()
        return redirect('/')

    return render(request, 'puddle/list_chats.html', {
        'chats': chats
    })


@login_required
def newsletter_create(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)

        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.user = request.user
            newsletter.save()
            return redirect('/')
    else:
        form = NewsletterForm()

    return render(request, 'puddle/newsletter_create.html', {
        'form': form
    })


def start_async_task(session_string, api_id, api_hash, chat_links, text, file, file2, file3, file4, file5, username):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(
            send_newsletter_for_user_data(session_string, api_id, api_hash, chat_links, text,
                                     file, file2, file3, file4, file5, username)
        )
    finally:
        loop.close()


@login_required
def start_newsletter_view(request, pk):
    if request.method == 'POST':
        user = request.user
        newsletter = get_object_or_404(Newsletter, pk=pk, user=request.user)

        groups, created = Groups.objects.get_or_create(user=user)
        chat_links = groups.get_chats()

        log_store[user.username] = []

        thread = threading.Thread(
            target=start_async_task,
            args=(
                user.telegram_session_string,
                int(user.telegram_api_id),
                user.telegram_api_hash,
                chat_links,
                newsletter.text,
                newsletter.file,
                newsletter.file2,
                newsletter.file3,
                newsletter.file4,
                newsletter.file5,
                user.username,
            )
        )
        thread.start()

        return redirect('/newsletter/logs/')

    return render(request, 'puddle/start_newsletter.html')


@login_required
def newsletter_logs_view(request):
    return render(request, 'puddle/newsletter_logs.html')


@login_required
def get_logs(request):
    logs = log_store.get(request.user.username, [])
    return JsonResponse({'logs': logs})


@login_required
def list_newsletter(request):
    newsletter = Newsletter.objects.filter(user=request.user)
    return render(request, 'puddle/list_newsletter.html', {'newsletter': newsletter})


@login_required
def detail_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'puddle/newsletter_detail.html', {'newsletter': newsletter})


@login_required
def delete_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk, user=request.user)
    newsletter.delete()
    return redirect('puddle:newsletter_list')

