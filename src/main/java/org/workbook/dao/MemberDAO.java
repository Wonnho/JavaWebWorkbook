package org.workbook.dao;

import java.sql.Connection;

import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class MemberDAO {
    public boolean login(String id, String pw) throws Exception {

        Connection conn = ConnectionUtil.INSTANCE.getConnection(); // 네가 만든 커넥션 유틸

        String sql = "SELECT * FROM tbl_member WHERE todoid=? AND todopw=?";

        PreparedStatement ps = conn.prepareStatement(sql);
        ps.setString(1, id);
        ps.setString(2, pw);

        ResultSet rs = ps.executeQuery();

        return rs.next(); // 있으면 true (로그인 성공)
    }
}
