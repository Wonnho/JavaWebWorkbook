package org.workbook.todo.dto;

import java.time.LocalDate;

public class TodoDTO {
    private Long tno;
    private String title;
    private LocalDate dueDate;

    private boolean done;

    public Long getTno() {
        return tno;
    }

    public void setTno(Long tno) {
        this.tno = tno;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }

    public boolean isDone() {
        return done;
    }

    public void setDone(boolean done) {
        this.done = done;
    }


    public String toString() {
        return "TodoDTO{" +
                "tno=" + tno +
                ", title='"+ title + '\'' +
                ", dueDate=" + dueDate +
                ", done=" + done +
                '}';
    }
}
