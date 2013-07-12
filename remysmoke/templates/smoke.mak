<%inherit file="local:templates.master"/>

<div>
  <form action="/register_smoke" method="POST" enctype="multipart/form-data" id="smokeform">
    <ul id="smokeform">
      <li class="odd required">
        <label for="date">Date</label>
        <input type='datetime' name='date' id='date' value="${context.get('date', '')}" required />
        <span class="error" id="error:date">
          ${context.get('error.date', '')}
        </span>
      </li>
      <li class="even required">
        <label for="justification">Justification</label>
        <textarea name="justification" id='justification' required>${context.get('justification', '')}</textarea>
        <span class="error" id="error:justification">
          ${context.get('error.justification', '')}
        </span>
      </li>
    </ul>

    <input type="submit" value="Save" />
  </form>
</div>
