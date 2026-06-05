package com.stock.marketwatcher.controller;

import com.stock.marketwatcher.domain.Board;
import com.stock.marketwatcher.dto.BoardDTO;
import com.stock.marketwatcher.dto.PageRequestDTO;
import com.stock.marketwatcher.dto.PageResponseDTO;
import com.stock.marketwatcher.service.BoardService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import org.w3c.dom.stylesheets.LinkStyle;

import java.util.List;

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

    @PostMapping("/register")
    public String register(@Valid BoardDTO boardDTO, BindingResult  bindingResult, RedirectAttributes redirectAttributes) {

        log.info("board POst register .....................");
    if(bindingResult.hasErrors()) {
        log.info("hasErrors.............");
        redirectAttributes.addFlashAttribute("errors",bindingResult.getAllErrors());
        return "redirect:/board/register";
    }
    log.info(boardDTO);
    Long bno=boardService.register(boardDTO);
    redirectAttributes.addFlashAttribute("result",bno);
    return "redirect:/board/list";
    }

    @GetMapping("register")
    public void registerGET(){};

    @GetMapping({"/read","/modify"})
    public void read(@RequestParam("bno") Long bno, PageRequestDTO pageRequestDTO, Model model) {
      BoardDTO  boardDTO=boardService.readOne(bno);
      log.info("board DTO :", boardDTO);
      model.addAttribute("dto",boardDTO);
    }

    @PostMapping("/modify")
    public String modify(PageRequestDTO pageRequestDTO,
                                 @Valid BoardDTO boardDTO,
                                  BindingResult bindingResult,
                                  RedirectAttributes redirectAttributes){


        log.info("board modify post......." + boardDTO);

        if(bindingResult.hasErrors()) {
            log.info("has errors.......");

            String link = pageRequestDTO.getLink();

            redirectAttributes.addFlashAttribute("errors", bindingResult.getAllErrors() );

            redirectAttributes.addAttribute("bno", boardDTO.getBno());

            return "redirect:/board/modify?"+link;
        }

        boardService.modify(boardDTO);

        redirectAttributes.addFlashAttribute("result", "modified");

        redirectAttributes.addAttribute("bno", boardDTO.getBno());

        return "redirect:/board/read";
    }
    @PostMapping("/remove")
    public String remove(Long bno, RedirectAttributes redirectAttributes) {

        log.info("remove post.. " + bno);

        boardService.remove(bno);

        redirectAttributes.addFlashAttribute("result", "removed");

        return "redirect:/board/list";

    }


}

