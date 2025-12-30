---
title: Gallery
---

{% for file in site.static_files %}
  {% if file.path contains '/images/' %}
![{{ file.name }}]({{ file.path }})
  {% endif %}
{% endfor %}
