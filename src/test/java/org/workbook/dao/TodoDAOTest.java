package org.workbook.dao;

import org.junit.jupiter.api.BeforeEach;

public class TodoDAOTest {
    private TodoDAO todoDAO;

    @BeforeEach
    public void ready() {
        todoDAO=new TodoDAO();

    }

    public void testTime() throws Exception{
        System.out.println(todoDAO.getTime());
    }
}
