<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head>
    <title>todo list</title>
</head>
<body>
<h1>List Page</h1>

<ul>
    <c:forEach var="dto" items="${dtoList}">
        <li>
        <span>
        <a href="/todo/read?tno=${dto.tno}">${dto.tno}</a>
        </span>
        <span>${dto.title}</span>
         <span>${dto.dueDate}</span>
          <span> ${dto.done ? "Done": "NOT YET"}</span>
          </li>
    </c:forEach>
</ul>

<form action="/logout" method="post">
<button>LOGOUT</button>
</form>

</body>
</html>