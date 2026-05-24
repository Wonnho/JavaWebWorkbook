package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Board;
import lombok.extern.log4j.Log4j2;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;

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

    @Test
    public void deleteTest() {
        Long bno=1L;

        boardRepository.deleteById(bno);
    }
    @Test
    public void pageTest() {

        Pageable pageable =PageRequest.of(0,10, Sort.by("bno").descending());

         Page<Board> result=boardRepository.findAll(pageable);

         log.info("total count " + result.getTotalElements());

    }

    @Test
    public void searchTest1() {
     Pageable  pageable=PageRequest.of(1,10,Sort.by("bno").descending());

     boardRepository.search1(pageable);
    }

}
