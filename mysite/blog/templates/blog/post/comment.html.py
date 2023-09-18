{% extends "../base.html" %}
{% block title %} Add Comment {% endblock %}
{% block content %}
   {% if comment %}
      <h2> Your comment has been added </h2>
      <a href="{{ post.get_absolute_url }}">
          back to post
      </a>
   {% else %}
      {% include "./includes/comment_form.html" %}
   {% endif %}
{% endblock %}
     
