package com.example.springdemo;

import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

@RunWith(SpringRunner.class)
@SpringBootTest
@WebAppConfiguration
class SpringdemoApplicationTests {
    @Autowired
    private WebApplicationContext context;

    @Test
    public void testApplication(){
        MockMvc mockMvc = MockMvcBuilders.webAppContextSetup(context).build();
        try {
            Thread.sleep(60000);
            mockMvc.perform(MockMvcRequestBuilders.get("/get?keyword=命里有财&start=0&size=10&approach=relativity&" +
                    "hrefcontains=new.qq.com news.sohu.com&channel=travel ent&timestart=2020-01-08 00:00:00&timeend=2020-10-29 23:59:00")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/get?keyword=命里有财&start=0&size=10&approach=time&" +
                    "hrefcontains=new.qq.com news.sohu.com&channel=travel ent&timestart=2020-01-08 00:00:00&timeend=2020-10-29 23:59:00")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/get?keyword=命里有财&start=0&size=10&approach=relativity")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/get?keyword=命里有财为了凑满十个以上的字符数&start=0&size=10&approach=relativity")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/get?keyword=命里有财&start=0&size=10&approach=time&" +
                    "timestart=2020-01-08 00:00:00")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/get?keyword=命里有财&start=0&size=10&approach=time&" +
                    "timeend=2020-10-29 23:59:00")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/get?keyword=命里有财&start=0&size=10&approach=time")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/tags?tags=北海市,20;浙江,10&start=0&size=10&" +
                    "timestart=2020-01-01 00:00:00&timeend=2020-11-09 23:59:00")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/tags?tags=北海市,20;浙江,10&start=0&size=10")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/tags?tags=北海市,20;浙江,10&start=0&size=10&" +
                    "timeend=2020-11-09 23:59:00")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
            mockMvc.perform(MockMvcRequestBuilders.get("/tags?tags=北海市,20;浙江,10&start=0&size=10&" +
                    "timestart=2020-01-01 00:00:00")
                    .contentType(MediaType.APPLICATION_JSON_UTF8)
                    .accept(MediaType.APPLICATION_JSON_UTF8))
                    .andExpect(MockMvcResultMatchers.status().isOk());
        } catch (Exception e){
            e.printStackTrace();
        }

    }

}
