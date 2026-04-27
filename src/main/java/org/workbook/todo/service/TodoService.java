package org.workbook.todo.service;

import org.workbook.todo.dto.TodoDTO;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public enum TodoService {
    INSTANCE;

    public void register(TodoDTO todoDTO) {
        System.out.println("DEBUG......................" + todoDTO);
    }

    public List<TodoDTO> getList() {

        List<TodoDTO> todoDTOS= IntStream.range(0,10).mapToObj(k->{
            TodoDTO dto=new TodoDTO();
            dto.setTno((long)k);
            dto.setTitle("Todo..." +k);
            dto.setDueDate(LocalDate.now());
            return dto;
        }).collect(Collectors.toList());

        return todoDTOS;
    }
}
