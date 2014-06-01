<%inherit file="local:templates.master"/>

<%def name='head()'>
	<link href="/css/graph.css" media="screen" type="text/css" rel="stylesheet">
</%def>

<form action=${tg.url('graph')} class='chart'>
  <fieldset>
    <h2><span>Histogram</span></h2>
    <label for='weeks'>Range</label>
    <input name='weeks' id='weeks' type='range' min=1 max=52 value=${weeks if weeks else 1} />
    <input type='submit' name='histogram' id='time_submit' class='submit' value='Generate' />
  </fieldset>
  <fieldset>
    <h2><span>Punchcard</span></h2>
    <input type='submit' name='punchcard' id='punch_submit' class='submit' value='Generate' />
  </fieldset>
  <%include file='local:templates.user_picker'/>
</form>

<div style='height:230px'>
  ${widget | n}
</div>
