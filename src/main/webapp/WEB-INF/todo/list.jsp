<%@ page contentType="text/html; charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head>
    <title>todo list</title>
</head>
<body>
<h1>List Page</h1>

<ul>
    <c:forEach var="todo" items="${list}">
        <li>${todo.tno} | ${todo.title} | ${todo.dueDate}</li>
    </c:forEach>
</ul>

</body>
</html>