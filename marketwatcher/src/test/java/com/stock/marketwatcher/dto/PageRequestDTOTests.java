package com.stock.marketwatcher.dto;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class PageRequestDTOTests {

    @Test
    void getLinkOmitsBlankSearchParameters() {
        PageRequestDTO pageRequestDTO = PageRequestDTO.builder()
                .page(2)
                .size(20)
                .type("")
                .keyword("")
                .build();

        assertThat(pageRequestDTO.getLink()).isEqualTo("page=2&size=20");
    }

    @Test
    void getLinkIncludesEncodedSearchParameters() {
        PageRequestDTO pageRequestDTO = PageRequestDTO.builder()
                .page(1)
                .size(10)
                .type("tc")
                .keyword("spring boot")
                .build();

        assertThat(pageRequestDTO.getLink()).isEqualTo("page=1&size=10&type=tc&keyword=spring+boot");
    }
}
