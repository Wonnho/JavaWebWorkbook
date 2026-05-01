<%@ page contentType="text/html; charset=UTF-8" language="java" %>

<html>
<head>
    <title>Todo read</title>
</head>
<body>
<div>
<input type="text" name="tno" value="${dto.tno}" readOnly> </div>

<div>
<input type="text" name="title" value="${dto.title}" readOnly>
</div>

<div>
<input type="date" name="dueDate" value="${dto.dueDate}"></div>
<div>
<input type="checkbox" name="done" ${dto.done ? "checked":""} readOnly>
</div>

<div>

<a href="/todo/modify?tno=${dto.tno}">Modify/Remove</a>
<a href="/todo/list">List</a>
</div>
</body>
</html>