package org.workbook.dao;

import org.junit.jupiter.api.Test;

public class MemberDAOTest {

    @Test
    public void testLogin() throws Exception {
        MemberDAO dao=new MemberDAO();
        boolean result= dao.login("dataEngineer","DE4433");
        System.out.println("result: " +result);
    }
}
