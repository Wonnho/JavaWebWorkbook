package com.stock.marketwatcher.service;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.dto.BoardDTO;
import com.stock.marketwatcher.repository.BoardRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
@Log4j2
@RequiredArgsConstructor
@Transactional
public class BoardServiceImpl implements BoardService {
    private final ModelMapper modelMapper;

    private final BoardRepository boardRepository;

    @Override
    public Long register(BoardDTO boardDTO) {

        Board board=modelMapper.map(boardDTO, Board.class);
        Long bno=boardRepository.save(board).getBno();
        return bno;
    }
}
