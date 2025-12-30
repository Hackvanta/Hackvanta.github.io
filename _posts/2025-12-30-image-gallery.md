---
title: "Image Feed"
date: 2025-12-30
layout: post
---

{% raw %}
{% for file in site.static_files %}
  {% if file.path contains '_/images' %}
![{{ file.name }}]({{ site.url }}{{ file.path }})
  {% endif %}
{% endfor %}
{% endraw %}