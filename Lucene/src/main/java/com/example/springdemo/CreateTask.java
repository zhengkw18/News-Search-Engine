package com.example.springdemo;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.sql.SQLException;


@Component
public class CreateTask {
    CreateIndex createIndex;

    public CreateTask() throws IOException {
        createIndex = new CreateIndex();
    }

    @Scheduled(fixedDelay = 1000)
    public void getTask() throws IOException, SQLException {
        createIndex.createAppend();
    }
}