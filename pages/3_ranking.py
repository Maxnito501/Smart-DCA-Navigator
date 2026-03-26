from utils.data_fetcher import fetch_price, fetch_rsi, fetch_ema200

def generate_ranking_data(stocks, mode="core"):
    data = []
    for stock in stocks[:10]:
        price = fetch_price(stock)
        rsi = fetch_rsi(stock)
        ema200 = fetch_ema200(stock)
        
        if price is None or rsi is None:
            continue
            
        if mode == "core":
            score = 0
            if rsi < 30:
                score += 30
            elif rsi < 40:
                score += 20
            if price < ema200:
                score += 25
            score += np.random.uniform(0, 10)
            compare_ema = "ต่ำกว่า" if price < ema200 else "สูงกว่า"
        else:
            score = 0
            if rsi < 30:
                score += 25
            compare_ema = "-"
        
        data.append({
            "หุ้น": stock,
            "ราคา": price,
            "RSI": rsi,
            "EMA200": ema200,
            "เทียบ EMA200": compare_ema,
            "คะแนน": int(score)
        })
    
    df = pd.DataFrame(data)
    return df.sort_values("คะแนน", ascending=False).reset_index(drop=True)
