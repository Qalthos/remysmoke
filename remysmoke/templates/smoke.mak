<%inherit file="local:templates.master"/>

<%def name='head()'>
	<script src="/js/form_toggle.js" type="text/javascript"></script>
</%def>

<div>
  <form action="/register_smoke" method="POST" enctype="multipart/form-data" id="smokeform">
    <label for="date">Date:</label>
    <input id='date' type='datetime' name='date' class='text' value="${context.get('date', '')}" required />

    <span class="error" id="error:date">
      ${context.get('error.date', '')}
    </span>

    <label for="justification">Justification:</label>
    <input id='justification' type='text' name="justification" class='text' value="${context.get('justification', '')}" required></input>

    <span class="error" id="error:justification">
      ${context.get('error.justification', '')}
    </span>

    <input id='nosmoke' type="checkbox" name="nosmoke" class='check' />
    <label for='nosmoke'>I did not smoke today</label>

    <input type="submit" class='submit' value="Save" />
  </form>
</div>
