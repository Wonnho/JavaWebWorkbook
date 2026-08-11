package com.stock.marketwatcher.repository;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.domain.BoardImage;
import com.stock.marketwatcher.dto.BoardListAllDTO;
import com.stock.marketwatcher.dto.BoardListReplyCountDTO;
import jakarta.transaction.Transactional;
import lombok.extern.log4j.Log4j2;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.test.annotation.Commit;

import java.util.Optional;
import java.util.UUID;
import java.util.stream.IntStream;

import static com.stock.marketwatcher.domain.QBoard.board;

@SpringBootTest
@Log4j2
public class BoardRepositoryTests {
    @Autowired
    private BoardRepository boardRepository;

    @Autowired
    private ReplyRepository replyRepository;

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

    @Test
    public void testSearchAll() {

        String[] types = {"t","c","w"};

        String keyword = "1";

        Pageable pageable = PageRequest.of(0,10, Sort.by("bno").descending());

        Page<Board> result = boardRepository.searchAll(types, keyword, pageable );

    }

    @Test
    public void testSearchAll2() {

        String[] types = {"t","c","w"};

        String keyword = "1";

        Pageable pageable = PageRequest.of(0,10, Sort.by("bno").descending());

        Page<Board> result = boardRepository.searchAll(types, keyword, pageable );

        //total pages
        log.info(result.getTotalPages());

        //pag size
        log.info(result.getSize());

        //pageNumber
        log.info(result.getNumber());

        //prev next
        log.info(result.hasPrevious() +": " + result.hasNext());

        result.getContent().forEach(board -> log.info(board));
    }

    @Test
    public void testSearchReplyCount() {

        String[] types = {"t","c","w"};

        String keyword = "1";

        Pageable pageable = PageRequest.of(0,10, Sort.by("bno").descending());

        Page<BoardListReplyCountDTO> result = boardRepository.searchWithReplyCount(types, keyword, pageable );

        //total pages
        log.info(result.getTotalPages());
        //pag size
        log.info(result.getSize());
        //pageNumber
        log.info(result.getNumber());
        //prev next
        log.info(result.hasPrevious() +": " + result.hasNext());

        result.getContent().forEach(board -> log.info(board));
    }

    @Test
    public void testInsertWithImages() {
        Board board=Board.builder()
                .title("Image test")
                .content("upload image")
                .writer("tester")
                .build();

        for (int k=0;k<3;k++) {
            board.addImage(UUID.randomUUID().toString(),"file"+k+".png");
        }

        boardRepository.save(board);

    }

    @Transactional
    @Test
    public void testReadWithImages() {
        // 이미지 달린 게시글을 먼저 저장 후, 생성된 bno 로 조회
        Board saved = Board.builder()
                .title("read image test")
                .content("read image content")
                .writer("tester")
                .build();
        for (int k = 0; k < 3; k++) {
            saved.addImage(UUID.randomUUID().toString(), "file" + k + ".png");
        }
        Long bno = boardRepository.save(saved).getBno();

        Optional<Board> result = boardRepository.findByWithImages(bno);
        Board board = result.orElseThrow();
        log.info(board);
        log.info("-------------------");
        for (BoardImage boardImage : board.getImageSet()) {
            log.info(boardImage);
        }
    }
    @Transactional
    @Test
    public void testModifyImages() {
        // 이미지 3개로 저장
        Board saved = Board.builder()
                .title("modify image test")
                .content("modify image content")
                .writer("tester")
                .build();
        for (int k = 0; k < 3; k++) {
            saved.addImage(UUID.randomUUID().toString(), "file" + k + ".png");
        }
        Long bno = boardRepository.save(saved).getBno();

        // 이미지 2개로 교체
        Optional<Board> result = boardRepository.findByWithImages(bno);
        Board board = result.orElseThrow();
        board.clearImages();
        for (int k = 0; k < 2; k++) {
            board.addImage(UUID.randomUUID().toString(), "updatefile" + k + ".png");
        }
        boardRepository.save(board);
    }
    @Transactional
    @Commit
    @Test
  public  void testRemoveAll() {
        Long bno=1L;

        replyRepository.deleteByBoard_Bno(bno);
        boardRepository.deleteById(bno);
    }

@Test
    public void testInsertAll() {
        for(int k=1;k<=100;k++) {
             Board board=Board.builder()
                    .title("Title.."+k)
                    .content("Content.."+k)
                    .writer("Writer.."+k)
                    .build();

             for (int z=0;z<3;z++) {
                 if(k%5==0) {
                     continue;
                 }
                 board.addImage(UUID.randomUUID().toString(),k+"file"+z+".png");
             }
             boardRepository.save(board);
        }
}

    @Transactional
    @Test
    public void testSearchImageReplyCount() {
        Pageable pageable = PageRequest.of(0,10,Sort.by("bno").descending());

        //boardRepository.searchWithAll(null,null,pageable);

        Page<BoardListAllDTO> result=boardRepository.searchWithAll(null,null,pageable);
        log.info("===================================");
        log.info(result.getTotalElements());
        result.getContent().forEach(boardListAllDTO -> log.info(boardListAllDTO));
    }
}
