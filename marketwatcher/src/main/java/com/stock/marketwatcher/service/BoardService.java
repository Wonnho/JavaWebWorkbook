package com.stock.marketwatcher.service;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.dto.*;

public interface BoardService {

    Long register(BoardDTO boardDTO);
    // why Long? check bno, Long bno=boardService.register(boardDTO); from BoardServiceTests

    BoardDTO readOne(Long bno);

    //BoardDTO modify(Long bno);
    void modify(BoardDTO boardDTO);

    void remove(Long bno);

    PageResponseDTO<BoardDTO> list(PageRequestDTO pageRequestDTO);

    PageResponseDTO listWithReplyCount(PageRequestDTO pageRequestDTO);

    PageResponseDTO<BoardListAllDTO> ListWithAll(PageRequestDTO pageRequestDTO);


    default Board dtoToEntity(BoardDTO boardDTO) {
        Board board = Board.builder()
                .bno(boardDTO.getBno())
                .title(boardDTO.getTitle())
                .content(boardDTO.getContent())
                .writer(boardDTO.getWriter())
                .build();

        if (boardDTO.getFileNames() != null) {
            boardDTO.getFileNames().forEach(fileName -> {
                String[] arr = fileName.split("_");
                board.addImage(arr[0], arr[1]);
            });
        }


        return board;
    }
}