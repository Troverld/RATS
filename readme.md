### RATS: Reliable Assistant for Targeted Solutions

#### What is RATS?

An assistant that helps you with your homework.

But it does not directly provide the answer —— sometimes, LLM responds with step-by-step solution.

What do we really want? A detailed proof? No! We only need the key idea behind the proof.

Target user: Everyone! (Especially those who study science)

#### How to use RATS?

First, install all libraries from `requirements.txt`.

Second, create a `.env` file in the root directory, and write the following things:

```
INFINI_BASE_URL="Your LLM API url"
INFINI_API_KEY="Your LLM API key"
```

You need to use your own keys. (Of course we won't reveal ours!)

Then, run `front.py`, and a graphical interface will be automatically created on your browser.

Finally, may follow the instructions on the interface, and enjoy the detailed hints provided by <font color="gold">RATS</font>!

![](https://cdn.luogu.com.cn/upload/image_hosting/8h77icn2.png)