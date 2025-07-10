from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_session_list, name='game_session_list'),
    path('session/<int:pk>/', views.game_session_detail, name='game_session_detail'),

    # Hero URLs
    path('session/<int:game_session_pk>/heroes/', views.hero_list, name='hero_list'),
    path('session/<int:game_session_pk>/heroes/add/', views.hero_create, name='hero_create'),
    path('heroes/<int:pk>/edit/', views.hero_update, name='hero_update'),
    path('heroes/<int:pk>/delete/', views.hero_delete, name='hero_delete'),
    path('heroes/<int:pk>/', views.hero_detail, name='hero_detail'),

    # Enemy URLs
    path('session/<int:game_session_pk>/enemies/', views.enemy_list, name='enemy_list'),
    path('session/<int:game_session_pk>/enemies/add/', views.enemy_create, name='enemy_create'),
    path('enemies/<int:pk>/edit/', views.enemy_update, name='enemy_update'),
    path('enemies/<int:pk>/delete/', views.enemy_delete, name='enemy_delete'),
    path('enemies/<int:pk>/', views.enemy_detail, name='enemy_detail'),

    # Encounter URLs
    path('session/<int:game_session_pk>/encounters/', views.encounter_list, name='encounter_list'),
    path('session/<int:game_session_pk>/encounters/add/', views.encounter_create, name='encounter_create'),
    path('encounters/<int:pk>/edit/', views.encounter_update, name='encounter_update'),
    path('encounters/<int:pk>/delete/', views.encounter_delete, name='encounter_delete'),
    path('encounters/<int:pk>/', views.encounter_detail, name='encounter_detail'),
    path('encounters/<int:pk>/start/', views.start_encounter, name='start_encounter'),
    path('encounters/<int:pk>/next_turn/', views.next_turn, name='next_turn'),
    path('encounters/<int:pk>/attack/', views.attack, name='attack'),
    path('encounters/<int:pk>/heal/', views.heal, name='heal'),

    # Ability Check URLs
    path('roll_ability_check/<int:encounter_id>/<int:character_id>/<str:character_type>/<str:ability_name>/', views.roll_ability_check, name='roll_ability_check'),
    path('roll_general_ability_check/<int:character_id>/<str:character_type>/<str:ability_name>/', views.roll_general_ability_check, name='roll_general_ability_check'),
]
