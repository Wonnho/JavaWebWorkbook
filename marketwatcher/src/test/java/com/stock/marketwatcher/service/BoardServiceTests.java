package com.stock.marketwatcher.service;

import com.stock.marketwatcher.dto.BoardDTO;
import com.stock.marketwatcher.dto.PageRequestDTO;
import com.stock.marketwatcher.dto.PageResponseDTO;
import lombok.extern.log4j.Log4j2;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.UUID;

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
                .bno(1724L)
                .title("update title...")
                .content("update 1724 content")
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

    @Test
    public void testRegisterWithImages() {
        log.info(boardService.getClass().getName());

       BoardDTO boardDTO= BoardDTO.builder()
                .title("File...Sample Title...")
                .content("Sample Image content...")
                .writer("user1")
                .build();

        boardDTO.setFileNames(
                Arrays.asList(
                        UUID.randomUUID()+"_aaa.jpg",
                        UUID.randomUUID()+"_bbb.jpg",
                        UUID.randomUUID()+"_ccc.jpg"

                        ));
        Long bno=boardService.register(boardDTO);
        log.info("bno: "+bno);

    }

    @Test
    public void testReadAll() {
        Long bno=1724L;
        BoardDTO boardDTO=boardService.readOne(bno);
        log.info(boardDTO);
        for(String fileName: boardDTO.getFileNames()) {
            log.info(fileName);

        }
    }
}
