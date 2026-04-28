package org.workbook.domain;

import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

import java.time.LocalDate;


@Getter
@Builder
@ToString

public class TodoVO {
    private Long tno;
    private String title;
    private LocalDate dueDate;
    private boolean done;

    @Override
    public String toString() {
        return super.toString();
    }
}
