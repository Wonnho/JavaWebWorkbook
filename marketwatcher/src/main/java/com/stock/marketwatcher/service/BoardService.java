package com.stock.marketwatcher.service;

import com.stock.marketwatcher.dto.BoardDTO;

public interface BoardService {

    Long register(BoardDTO boardDTO);
    // why Long? check bno, Long bno=boardService.register(boardDTO); from BoardServiceTests

    BoardDTO readOne(Long bno);

   //BoardDTO modify(Long bno);
   void modify(BoardDTO boardDTO);
   void remove(Long bno);

}
