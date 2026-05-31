package com.stock.marketwatcher.service;

import com.stock.marketwatcher.dto.BoardDTO;
import com.stock.marketwatcher.dto.PageRequestDTO;
import com.stock.marketwatcher.dto.PageResponseDTO;
import lombok.extern.log4j.Log4j2;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
@Log4j2
public class BoardServiceTests {

    @Autowired
    private BoardService boardService;

    @Test
    public void registerTest() {
        log.info(boardService.getClass().getName());

     BoardDTO   boardDTO=BoardDTO.builder()
                .title("board title...")
                .content("test board")
                .writer("test builder")
                .build();

         Long bno=boardService.register(boardDTO);
         log.info("bno: "+ bno);
    }
    @Test
    public void modifyTest() {
        BoardDTO   boardDTO=BoardDTO.builder()
                .bno(2L)
                .title("modify title...")
                .content("test for modification on board")
//                .writer("test builder not user2")
                .build();

        boardService.modify(boardDTO);
    }

    @Test
    public void listTest() {
        PageRequestDTO pageRequestDTO=PageRequestDTO.builder()
                .type("tcw")
                .keyword("1")
                .page(1)
                .size(10)
                .build();

        PageResponseDTO<BoardDTO> responseDTO=boardService.list(pageRequestDTO);

        log.info(responseDTO);
    }
}
