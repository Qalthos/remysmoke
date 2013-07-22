<%inherit file="local:templates.master"/>

<%def name='head()'>
	<script src="/js/form_toggle.js" type="text/javasctipt" />
</%def>

<div>
  <form action="/register_smoke" method="POST" enctype="multipart/form-data" id="smokeform">
	<label for="date">Date:</label>
	<input id='date' type='datetime' name='date' class='text' value="${context.get('date', '')}" required />
	<br />
	<span class="error" id="error:date">
	  ${context.get('error.date', '')}
	</span>
	<br />
	<label for="justification">Justification:</label>
	<input id='justification' type='text' name="justification" class='text' value="${context.get('justification', '')}" required></input>
	<br />
	<span class="error" id="error:justification">
	  ${context.get('error.justification', '')}
	</span>
	<br />
	<input id='nosmoke' type="checkbox" name="nosmoke" class='check' />
	<label for='nosmoke'>I did not smoke today</label>
	<br />

    <input type="submit" id='submit' value="Save" />
  </form>
</div>
