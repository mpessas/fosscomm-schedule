<!DOCTYPE html>
<html>
  <head>
    <title>Πρόγραμμα</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" href="/schedule/schedule.css" type="text/css" media="screen"/>
    <script type="text/javascript" src="jquery-1.4.4.js"></script>
    <!-- <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>     -->
    <script type="text/javascript" src="schedule.js"></script>
  </head>
  <body>
    <header>
      <h1><a href="http://patras.fossocmm.gr">FOSSCOMM 2011 @ Patras</a></h1>
    </header>
    <h2>Πρόγραμμα</h2>
    <h2 id="title">{{title}}</h2>
    <h3 id="speaker">{{speaker}}</h3>
    <p id="summary">{{summary}}</p>
    <p id="details">{{day}}, {{start}} &#150 {{end}} @ {{room}}</p>
    <footer>
      <ul>
        <li><a href="http://www.patras-lug.gr/">&copy Patras Linux User Group</a></li>
        <li><a href="http://github.com/mpessas/">Code on Github</a></li>
      </ul>
    </footer>
  </body>
</html>
