package org.workbook.dao;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.workbook.domain.TodoVO;

import java.time.LocalDate;
import java.util.List;

public class TodoDAOTest {
    private TodoDAO todoDAO;

    @BeforeEach
    public void ready() {
        todoDAO=new TodoDAO();

    }

    public void testTime() throws Exception{
        System.out.println(todoDAO.getTime());
    }

    @Test
    public void testInsert() throws Exception {
        TodoVO todoVO= TodoVO.builder()
                .title("add record through todoVO")
                .dueDate(LocalDate.of(2026,4,29))
                .build();

        todoDAO.insert(todoVO);
    }

    @Test
    public void testList() throws Exception {
        List<TodoVO> list=todoDAO.selectAll();

        System.out.println("===== START =====");
        System.out.println("size = " + list.size());
        list.forEach(System.out::println);
        System.out.println("===== END =====");

        //list.forEach(vo -> System.out.println(vo));
    }
    @Test
    public void testOne() throws Exception {
        Long tno=1L;
        TodoVO vo=todoDAO.selectOne(tno);
        System.out.println(vo);
    }
    @Test
    public void deleteOne() throws Exception {
        Long tno=1L;
        todoDAO.deleteOne(tno);
       // System.out.println(vo);
    }

    @Test
    public  void testUpdateOne() throws Exception {
        TodoVO todoVO=TodoVO.builder()
                .tno(5L)
                .title("update 5 index of add record through todoVO")
                .dueDate(LocalDate.of(2026,4,29))
                .done(false)
                .build();

        todoDAO.updateOne(todoVO);
    }
}
