package com.stock.marketwatcher.controller;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.dto.BoardDTO;
import com.stock.marketwatcher.dto.PageRequestDTO;
import com.stock.marketwatcher.dto.PageResponseDTO;
import com.stock.marketwatcher.service.BoardService;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/board")
@RequiredArgsConstructor
@Log4j2
public class BoardController {
    private final BoardService boardService;

    @GetMapping("/list")
    public void list(PageRequestDTO pageRequestDTO, Model model) {

       PageResponseDTO<BoardDTO> responseDTO=boardService.list(pageRequestDTO);
    log.info(responseDTO);
    model.addAttribute("responseDTO",responseDTO);
    }
}
