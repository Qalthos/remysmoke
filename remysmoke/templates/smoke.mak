<%inherit file="local:templates.master"/>

<div>
  <form action="/register_smoke" method="POST" enctype="multipart/form-data" id="smokeform">
    <ul id="smokeform">
      <li class="odd required">
        <label for="date">Date:</label>
        <input type='datetime' name='date' class='text' value="${context.get('date', '')}" required />
        <span class="error" id="error:date">
          ${context.get('error.date', '')}
        </span>
      </li>
      <li class="even required">
        <label for="justification">Justification:</label>
        <input type='text' name="justification" class='text' value="${context.get('justification', '')}" required></input>
        <span class="error" id="error:justification">
          ${context.get('error.justification', '')}
        </span>
      </li>
    </ul>
	<input id='nosmoke' type="checkbox" name="nosmoke" class='check' />
	<label for='nosmoke'>I did not smoke today</label>
	<br />

    <input type="submit" id='submit' value="Save" />
  </form>
</div>
