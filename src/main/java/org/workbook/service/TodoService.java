package org.workbook.service;

import org.modelmapper.ModelMapper;
import org.workbook.dao.TodoDAO;
import org.workbook.domain.TodoVO;
import org.workbook.dto.TodoDTO;
import org.workbook.util.MapperUtil;

public enum TodoService {
    INSTANCE;
    private TodoDAO dao;
    private ModelMapper modelMapper;

    TodoService() {
        dao=new TodoDAO();
        modelMapper= MapperUtil.INSTANCE.get();

    }

    public void register(TodoDTO todoDTO) throws Exception {
        TodoVO todoVO=modelMapper.map(todoDTO,TodoVO.class);
        System.out.println("todoVO: " + todoVO);
        dao.insert(todoVO);
    }
}
