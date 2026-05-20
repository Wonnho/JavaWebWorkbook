package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Board;
import lombok.extern.log4j.Log4j2;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Optional;
import java.util.stream.IntStream;

@SpringBootTest
@Log4j2
public class BoardRepositoryTests {
    @Autowired
    private BoardRepository boardRepository;
    @Test
    public void InsertTest() {
        IntStream.rangeClosed(1,100).forEach(k -> {
            Board board=Board.builder()
                    .title("title..." +k)
                    .content("content..." + k)
                    .writer("user" +(k%10))
                    .build();

        Board result=boardRepository.save(board);
        log.info("BNO: " + result.getBno()) ;
        });

    }

    @Test
    public void selectTest() {
        Long bno=101L;

        Optional<Board> result=boardRepository.findById(bno);
      Board board=result.orElseThrow();
      log.info(board);
    }

    @Test
    public void updateTest(){
        // update via bno
        Long bno=100L;

        Optional<Board> result=boardRepository.findById(bno);
                 Board board=result.orElseThrow();
                 board.change("update title of bno 100","update content 100");
                 boardRepository.save(board);
    }

}
