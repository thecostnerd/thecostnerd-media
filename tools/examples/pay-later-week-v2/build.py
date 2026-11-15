"""Nov 19-25, 2026 (Pay Later week) rebuilt under the Nov 15 skill: 7 stories x (IG Reel hook A, IG trial hook B, TikTok hook C)."""
import json, copy, re
def A(f, s=0.6, x=0.5, y=0.5, delay=None, **kw):
    d = dict(f=f, s=s, x=x, y=y)
    if kw: d["args"] = kw
    if delay is not None: d["delay"] = delay
    return d
def H(bg, head, hl, art, sub, say, sticker=None):
    d = dict(bg=bg, head=head, hl=hl, hsize=128, art=art, sub=sub, dur=5, say=say)
    if sticker: d["sticker"] = sticker
    return d
def B(bg, head, hl, art, sub, say, dur=6):
    return dict(bg=bg, head=head, hl=hl, art=art, sub=sub, dur=dur, say=say)
def END(ig, tt, src, say_ig, say_tt):
    return dict(bg="ink", cta=True, end=ig, tt_end=tt, src=src, say=say_ig, tt_say=say_tt)

S = []

# 1. Thu Nov 19 - Walmart layaway
S.append(dict(n=1, date="2026-11-19", slug="walmart-layaway", file="Walmart Killed Layaway for This Button",
 hooks=[("surprise","Walmart killed layaway for THIS.","Walmart killed layaway for this."),
        ("ego","Grandma's layaway was SMARTER.","Your grandma's layaway was smarter than your app."),
        ("fear","Layaway is DEAD. This replaced it.","Layaway is dead. This button replaced it."),
        ("urgency","Black Friday layaway now starts with DEBT.","Black Friday layaway now starts with debt."),
        ("desire","Get it today. Pay nothing now?","Get it today, pay nothing now? Look closer.")],
 A=H("cream","Walmart KILLED layaway for this.",["KILLED"],[A("layaway_card",0.5,0.3,0.5),A("phone",0.5,0.74,0.5,delay=0.5,screen="PAY IN 4")],"2021: out with layaway, in with pay-later.","Walmart killed layaway for this.",None),
 B=H("ink","Grandma's layaway was SMARTER.",["SMARTER."],[A("layaway_card",0.62)],"Same small payments. One big difference.","Your grandma's layaway was smarter than your app."),
 C=H("yellow","Layaway is DEAD. This replaced it.",["DEAD."],[A("phone",0.6,0.5,0.5,screen="PAY IN 4")],"Walmart made the switch in 2021.","Layaway is dead. This button replaced it."),
 body=[B("ink","Layaway: you PAID first.",["PAID"],[A("layaway_card",0.62)],"Small payments. The store held the item until it was paid off.","Layaway was simple: you paid first, and the store held your stuff."),
       B("cream","Walmart killed it once: 2006.",["2006."],[A("calendar",0.6,top="DROPPED",big="2006")],"Then brought it back during the Great Recession (Quartz).","Walmart dropped it in two thousand six, then brought it back in the recession."),
       B("yellow","2021: hello, AFFIRM.",["AFFIRM."],[A("phone",0.6,screen="PAY IN 4")],"Walmart swapped layaway for Affirm's pay-later (Marketplace, 2022).","In twenty twenty-one, Walmart swapped layaway for pay later with Affirm."),
       B("ink","Same payments. FLIPPED order.",["FLIPPED"],[A("pay4",0.7,amt="$75")],"You get the item now, and the debt now too. Example prices.","Same small payments, flipped order. You get the thing now, and the debt now too."),
       B("red","The watchdog's verdict: DEBT now.",["DEBT"],[A("stamp",0.55,txt="DEBT",color="yellow")],"The US consumer-finance watchdog's director called it the new layaway, with the debt up front.","Even America's consumer finance watchdog called it the new layaway, with the debt up front.",7),
       B("cream","Could you pay CASH today?",["CASH"],[A("big_button",0.62,txt="CASH TODAY?")],"The layaway rule: only split it if you could pay in full right now.","So use the layaway rule: only split it if you could pay cash today."),
       END("Save this + send it to whoever still misses layaway.","Follow for Part 2: Apple tried this. Then it quit.","Sources: Marketplace 2022 · Quartz · FOX 35/LendingTree","Save this, and send it to whoever still misses layaway.","Follow for part two: Apple tried this, then quit.")],
 ig="Walmart killed layaway for this 👇\n\nLayaway was simple: you paid first, and the store held your stuff. Walmart dropped it in 2006, brought it back in the recession, then in 2021 swapped it for Affirm's pay-later.\n\nSame small payments, flipped order: you get the item now, and the debt now too. Even the US consumer-finance watchdog's director called it the new layaway, with the debt up front.\n\nThe layaway rule: only split it if you could pay cash today.\n\nDid your family ever use layaway? 👇 Send this to whoever still misses it.\n\nSources: Marketplace (Jan 2022), Quartz, FOX 35 / LendingTree. Example prices on screen.\n\n#buynowpaylater #walmart #layaway #moneytips #personalfinance",
 tt="Walmart killed layaway for buy now pay later 🛒 Did your family use layaway? 👇 #buynowpaylater #walmart #layaway #moneytok"))

# 2. Fri Nov 20 - Apple Pay Later
S.append(dict(n=2, date="2026-11-20", slug="apple-pay-later", file="Apple Tried Pay Later Then Quit After 15 Months",
 hooks=[("surprise","Apple tried pay-later. Then QUIT.","Apple tried pay later. Then quit."),
        ("fear","Your Apple Pay loan? NOT Apple.","That Apple Pay loan isn't from Apple anymore."),
        ("desire","Apple quit after 15 months. WHY?","Apple quit pay later after fifteen months. Why?"),
        ("ego","Even APPLE couldn't make it work.","Even Apple couldn't make pay later work."),
        ("urgency","Before you tap pay later: CHECK this.","Before you tap pay later, check this.")],
 A=H("cream","Apple tried pay-later. Then QUIT.",["QUIT."],[A("phone",0.55,0.32,0.5,screen="PAY LATER"),A("stamp",0.45,0.72,0.5,delay=0.5,txt="QUIT")],"Apple Pay Later: March 2023 to June 2024.","Apple tried pay later. Then quit.",None),
 B=H("ink","Your Apple Pay loan? NOT Apple.",["NOT"],[A("phone",0.62,screen="PAY IN 4")],"The button stayed. The lender changed.","That Apple Pay loan isn't from Apple anymore."),
 C=H("yellow","Apple quit after 15 months. WHY?",["WHY?"],[A("phone",0.55,0.4,0.5,screen="PAY LATER"),A("question",0.35,0.76,0.45,delay=0.5)],"Apple Pay Later, 2023 to 2024.","Apple quit pay later after fifteen months. Why?"),
 body=[B("ink","2023: up to $1,000 at 0%.",["$1,000"],[A("phone",0.6,screen="$1,000",sub="4 PAYMENTS")],"Four payments over six weeks, no interest or fees (Apple Support).","March twenty twenty-three: Apple Pay Later. Up to a thousand dollars, four payments, six weeks, no interest."),
       B("cream","Apple was the LENDER.",["LENDER."],[A("money_stack",0.6,label="APPLE $")],"The loans were backed directly by Apple (Washington Times, 2024).","And Apple lent the money itself."),
       B("red","June 2024: CLOSED.",["CLOSED."],[A("stamp",0.6,txt="CLOSED",color="yellow")],"Apple stopped making new pay-later loans on June 17, 2024 (AP).","June twenty twenty-four: no more new loans. About fifteen months in."),
       B("yellow","The button STAYED.",["STAYED."],[A("big_button",0.62,txt="PAY LATER")],"Now banks, card issuers and Affirm do the lending through Apple Pay.","The button stayed. Now banks and Affirm do the lending."),
       B("ink","Apple kept the button. Dropped the RISK.",["RISK."],[A("phone",0.5,0.32,0.5,screen="PAY LATER"),A("arrow",0.4,0.72,0.5,delay=0.4)],"\"It just won't be taking the risk itself.\" (Android Authority)","Apple kept the button, and handed off the risk.",7),
       B("cream","Before you tap: WHO do you owe?",["WHO"],[A("magnifier",0.58,txt="WHO?")],"The name on the loan is who you pay, and whose fees apply.","So before you tap, check whose loan it is. That's who you owe."),
       END("Save this for your next checkout.","Follow for Part 2: what people now pay for in 4.","Sources: Apple Support · AP · Washington Times · Android Authority","Save this for your next checkout.","Follow for part two: what people now split into four.")],
 ig="Apple tried buy now, pay later. Then it quit 📱\n\nApple Pay Later launched in March 2023: up to $1,000, four payments over six weeks, no interest, with Apple lending the money itself. On June 17, 2024, it stopped making new loans.\n\nThe button stayed. Now banks, card issuers and Affirm do the lending. Apple kept the button and handed off the risk.\n\nBefore you tap, check whose loan it is. That's who you owe.\n\nWould you trust a phone company with your loan? 👇\n\nSources: Apple Support, AP, Washington Times, Android Authority.\n\n#applepaylater #buynowpaylater #applepay #moneytips #personalfinance",
 tt="Apple pay later shut down after 15 months 📱 Would you trust a phone company with your loan? 👇 #applepaylater #buynowpaylater #moneytok"))

# 3. Sat Nov 21 - Groceries
S.append(dict(n=3, date="2026-11-21", slug="groceries-pay-in-4", file="People Are Paying for Eggs in 4 Payments Now",
 hooks=[("fear","People are paying for EGGS in 4.","People are paying for eggs in four payments."),
        ("ego","3 in 10 pay-later users do THIS.","Three in ten pay later users do this."),
        ("surprise","Pay-later for groceries DOUBLED.","Pay later for groceries just doubled."),
        ("urgency","Your groceries now have DUE DATES.","Your groceries now have due dates."),
        ("desire","Split your groceries? Read this FIRST.","Thinking of splitting your groceries? Read this first.")],
 A=H("cream","People pay for EGGS in 4 now.",["EGGS"],[A("egg_carton",0.7)],"29% of pay-later users have bought groceries with it.","People are paying for eggs in four payments.",None),
 B=H("ink","3 in 10 pay-later users do THIS.",["THIS."],[A("egg_carton",0.62,label="")],"And it's more than double what it was in 2024.","Three in ten pay later users do this."),
 C=H("yellow","Pay-later for groceries DOUBLED.",["DOUBLED."],[A("bars2",0.6,a="14%",b="29%",la="2024",lb="2026",ha=0.48,hb=1.0)],"Share of pay-later users who've bought groceries with it.","Pay later for groceries just doubled."),
 body=[B("ink","29% used it for GROCERIES.",["GROCERIES."],[A("egg_carton",0.62)],"Of pay-later users, LendingTree 2026 survey.","Twenty-nine percent of pay later users have used it for groceries."),
       B("yellow","It DOUBLED in two years.",["DOUBLED"],[A("bars2",0.6,a="14%",b="29%",la="2024",lb="2026",ha=0.48,hb=1.0)],"14% two years ago (LendingTree).","Two years ago, it was fourteen percent."),
       B("cream","Eaten by week 1. Paid by WEEK 6.",["WEEK 6."],[A("pay4",0.7,amt="$25",hit=3)],"Pay in 4 usually runs six weeks. Example prices.","The food is gone in a week. Payment four lands in week six."),
       B("ink","47% paid LATE last year.",["LATE"],[A("stamp",0.6,txt="LATE",color="red")],"Of pay-later users, up from 34% in 2024 (LendingTree).","And forty-seven percent of users paid late in the past year."),
       B("red","3 carts = 12 PAYMENTS.",["PAYMENTS."],[A("receipt",0.62,rows=(("Cart 1","x4"),("Cart 2","x4"),("Cart 3","x4")),total=("PAYMENTS","12"),title="EXAMPLE")],"Stack your weekly shops and the payments stack too.","Split three weekly shops, and you owe twelve payments at once.",7),
       B("yellow","Gone before payment 4? DON'T split.",["DON'T"],[A("big_button",0.62,txt="DON'T SPLIT")],"If it's used up before the last payment, pay for it now.","The rule: if it's gone before the last payment, don't split it."),
       END("Save this + send it to whoever does the grocery run.","Follow for Part 2: miss ONE payment, here's the fee.","Sources: LendingTree 2026 BNPL Report · Chain Store Age","Save this, and send it to whoever does the grocery run.","Follow for part two: miss one payment, here's the fee.")],
 ig="People are paying for eggs in 4 payments now 🥚\n\n29% of buy now, pay later users have used it for groceries, up from 14% two years ago. The food is gone in a week, but payment four lands in week six.\n\nAnd 47% of users paid late at least once in the past year.\n\nSplit three weekly shops and you owe 12 payments at once.\n\nThe rule: if it's gone before the last payment, don't split it.\n\nHave you ever split a grocery bill? 👇 Send this to whoever does the grocery run.\n\nSources: LendingTree 2026 Buy Now, Pay Later Report; Chain Store Age. Example prices on screen.\n\n#buynowpaylater #groceries #groceryprices #budgeting #personalfinance",
 tt="Buy now pay later for groceries doubled 🥚 Would you split a grocery bill? 👇 #buynowpaylater #groceries #moneytok #budgeting"))

# 4. Sun Nov 22 - Afterpay late fee (Ep 3 day)
S.append(dict(n=4, date="2026-11-22", slug="afterpay-late-fee", file="Miss One Afterpay Payment - Here Is the Bill",
 hooks=[("fear","Miss ONE Afterpay payment. The bill:","Miss one Afterpay payment. Here's the bill."),
        ("ego","0% interest? Only if you're NEVER late.","Zero percent? Only if you're never late."),
        ("surprise","A 0% loan that can cost 25%.","This zero percent loan can cost twenty-five percent."),
        ("urgency","Payment due Friday? Do this TODAY.","Payment due this week? Do this today."),
        ("desire","The free Afterpay button nobody uses.","There's a free Afterpay button almost nobody talks about.")],
 A=H("cream","Miss ONE Afterpay payment.",["ONE"],[A("phone",0.55,0.32,0.5,screen="PAY IN 4"),A("price_tag",0.45,0.72,0.46,delay=0.5,txt="+$8")],"Here's what it can cost.","Miss one Afterpay payment. Here's the bill.",None),
 B=H("ink","0% interest? Only if NEVER late.",["NEVER"],[A("pie",0.6,frac=0.25,label="25%")],"The fee cap is a quarter of your order.","Zero percent? Only if you're never late."),
 C=H("yellow","A 0% loan that can cost 25%.",["25%."],[A("pie",0.6,frac=0.25,label="25%")],"Afterpay's own late-fee cap.","This zero percent loan can cost twenty-five percent."),
 body=[B("ink","0% interest. IF you're on time.",["IF"],[A("phone",0.6,screen="PAY IN 4",sub="0% INTEREST")],"Afterpay Pay in 4: four payments, no interest when paid on time.","Afterpay says pay in four, zero interest. True, if you're on time."),
       B("cream","Up to $8 per MISS.",["$8"],[A("price_tag",0.6,txt="$8")],"After a 10-day grace period, a late fee of up to $8 per missed payment (Afterpay; NerdWallet).","Miss one, and after ten days there's a late fee, up to eight dollars."),
       B("yellow","Capped at 25% of your ORDER.",["ORDER."],[A("pie",0.6,frac=0.25,label="25%")],"Total late fees per order never exceed 25% of the order value (Afterpay).","The cap is twenty-five percent of your order."),
       B("ink","$40 order. $10 in FEES.",["FEES."],[A("receipt",0.62,rows=(("Order","$40"),("Late fees","+$10")),total=("TOTAL","$50"),title="EXAMPLE")],"Example prices: the 25% cap on a $40 order.","On a forty dollar order, that's ten dollars in fees. A quarter of what you bought.",7),
       B("cream","Twist: you can MOVE one payment free.",["MOVE"],[A("calendar",0.6,top="MOVE 1",big="FREE")],"Afterpay lets you reschedule one Pay in 4 payment per order at no cost (NerdWallet).","Twist: Afterpay lets you reschedule one payment per order, for free."),
       B("red","Short this week? RESCHEDULE.",["RESCHEDULE."],[A("big_button",0.62,txt="RESCHEDULE")],"Do it before a late fee lands.","Short this week? Reschedule it, before a late fee lands."),
       END("Save this before your next pay-in-4.","Follow for Part 2: does pay-in-4 even help your credit?","Sources: Afterpay Help & Installment Agreement · NerdWallet","Save this before your next pay in four.","Follow for part two: does it even help your credit?")],
 ig="Miss one Afterpay payment. Here's the bill 👇\n\nAfterpay's Pay in 4 is 0% interest, if you're on time. Miss a payment and, after a 10-day grace period, there's a late fee of up to $8. Total late fees on one order are capped at 25% of the order value.\n\nOn a $40 order, that's up to $10 in fees: a quarter of what you bought.\n\nThe twist: Afterpay lets you reschedule one payment per order for free. Short this week? Reschedule it before a late fee lands.\n\nThe full story of who really pays for \"0% interest\" is on our YouTube channel today.\n\nDid you know you could reschedule? 👇\n\nSources: Afterpay Help Center and US Installment Agreement; NerdWallet. Example prices on screen.\n\n#afterpay #buynowpaylater #latefees #moneytips #personalfinance",
 tt="Afterpay late fee explained 💸 0% interest, until you're late. Did you know you can reschedule? 👇 #afterpay #buynowpaylater #moneytok"))

# 5. Mon Nov 23 - credit blind spot
S.append(dict(n=5, date="2026-11-23", slug="credit-blind-spot", file="Paid On Time - Your Credit Score Never Saw It",
 hooks=[("surprise","Paid on time? Your credit NEVER saw it.","Paid on time? Your credit never saw it."),
        ("ego","Your bank can't SEE your pay-in-4s.","Your bank can't see your pay in fours."),
        ("fear","Your pay-later loans are INVISIBLE.","Your pay later loans are invisible. Problem."),
        ("urgency","Applying for a loan soon? Read this.","Applying for a loan soon? Read this first."),
        ("desire","Want pay-in-4 to build credit? Look.","Want pay in four to build your credit? Look.")],
 A=H("cream","Paid on time? Your credit NEVER saw it.",["NEVER"],[A("credit_gauge",0.7)],"Most pay-in-4 loans aren't reported to credit bureaus.","Paid on time? Your credit never saw it.",None),
 B=H("ink","Your bank can't SEE your pay-in-4s.",["SEE"],[A("credit_gauge",0.66,note="BLIND SPOT")],"The Federal Reserve calls it a blind spot.","Your bank can't see your pay in fours."),
 C=H("yellow","Your pay-later loans are INVISIBLE.",["INVISIBLE."],[A("credit_gauge",0.66,note="INVISIBLE")],"Federal Reserve, August 2026.","Your pay later loans are invisible. Problem."),
 body=[B("ink","Most aren't REPORTED.",["REPORTED."],[A("credit_gauge",0.66)],"Most pay-in-4 loans still aren't reported to the major bureaus (Federal Reserve, Aug 2026).","Most pay in four loans still aren't reported to the big credit bureaus."),
       B("cream","On time? Usually NO credit.",["NO"],[A("credit_gauge",0.66,val=0.5,note="NO CREDIT")],"If a lender doesn't report, on-time payments can't build your score.","So paying on time usually doesn't build your score."),
       B("red","The debt is real. Just HIDDEN.",["HIDDEN."],[A("receipt",0.62,rows=(("App 1","$75 x 3"),("App 2","$40 x 4"),("App 3","$60 x 2")),total=("OWED","$505"),title="EXAMPLE")],"Your bank, landlord or next lender may have no idea (PYMNTS). Example prices.","But the debt is real. Your landlord or next lender can't see it.",7),
       B("yellow","24% run SEVERAL at once.",["SEVERAL"],[A("phone",0.5,0.3,0.5,screen="PAY IN 4"),A("phone",0.5,0.7,0.5,delay=0.3,screen="PAY IN 4")],"Of pay-later users, carrying multiple loans at once (LendingTree 2026).","And twenty-four percent of users juggle more than one at once."),
       B("ink","The only tracker? YOU.",["YOU."],[A("magnifier",0.58,txt="TOTAL?")],"No bureau adds them up for you.","That means the only one tracking your total is you."),
       B("cream","One list. Every DUE DATE.",["DUE"],[A("checklist",0.66,rows=("EVERY APP","EVERY DUE DATE","ONE TOTAL"))],"Keep it where you'll see it before you tap buy.","Keep one list: every app, every due date, one total."),
       END("Save this + send it to the friend with three apps.","Follow for Part 2: the Black Friday bill due on Christmas.","Sources: Federal Reserve (Aug 2026) · PYMNTS · LendingTree 2026","Save this, and send it to the friend with three apps.","Follow for part two: the Black Friday bill due on Christmas.")],
 ig="Paid on time? Your credit score probably never saw it 📉\n\nMost pay-in-4 loans still aren't reported to the major credit bureaus, according to the Federal Reserve's August 2026 analysis. So on-time payments usually don't build your score.\n\nBut the debt is real, and your bank, landlord or next lender may not see it either. 24% of pay-later users carry more than one loan at once.\n\nThe only one tracking your total is you. Keep one list: every app, every due date, one total.\n\nHow many pay-later apps do you have? 👇 Send this to the friend with three.\n\nSources: Federal Reserve Consumer & Community Context (Aug 2026); PYMNTS; LendingTree 2026. Example prices on screen.\n\n#buynowpaylater #creditscore #klarna #moneytips #personalfinance",
 tt="Does buy now pay later build credit? Usually not 📉 How many pay later apps do you have? 👇 #buynowpaylater #creditscore #moneytok #personalfinance"))

# 6. Tue Nov 24 - Black Friday TV Christmas
S.append(dict(n=6, date="2026-11-24", slug="black-friday-christmas-bill", file="Your Black Friday TV Bills You on Christmas Day",
 hooks=[("surprise","Your Black Friday TV bills you on CHRISTMAS.","Your Black Friday TV bills you on Christmas."),
        ("ego","Black Friday deal. JANUARY bill.","Black Friday deal. January bill."),
        ("urgency","Before Black Friday, check this DATE.","Before Black Friday, check this one date."),
        ("fear","4 in 10 shoppers will SPLIT it.","Four in ten shoppers plan to split it."),
        ("desire","Want the deal without the January bill?","Want the deal without the January bill?")],
 A=H("cream","Your Black Friday TV bills you on CHRISTMAS.",["CHRISTMAS."],[A("tv",0.5,0.3,0.5,txt="$300"),A("calendar",0.45,0.73,0.5,delay=0.5,top="DEC",big="25")],"Pay in 4, starting Black Friday. Example prices.","Your Black Friday TV bills you on Christmas.",None),
 B=H("ink","Black Friday deal. JANUARY bill.",["JANUARY"],[A("calendar",0.6,top="JAN",big="8")],"Example: the last of four payments.","Black Friday deal. January bill."),
 C=H("yellow","Before Black Friday, check this DATE.",["DATE."],[A("calendar",0.6,top="DEC",big="25")],"Pay in 4, starting Nov 27. Example prices.","Before Black Friday, check this one date."),
 body=[B("ink","$300 TV? 4 payments of $75.",["$75."],[A("tv",0.5,0.3,0.5,txt="$300"),A("price_tag",0.42,0.73,0.46,delay=0.4,txt="$75")],"Example prices.","Example: a three hundred dollar TV, pay in four. Seventy-five dollars, four times."),
       B("cream","Payment 1: BLACK FRIDAY.",["FRIDAY."],[A("calendar",0.6,top="NOV",big="27")],"Black Friday 2026 is November 27.","Payment one, Black Friday, November twenty-seventh."),
       B("red","Payment 3: CHRISTMAS DAY.",["CHRISTMAS"],[A("calendar",0.6,top="DEC",big="25",color="yellow")],"Every two weeks: Dec 11, then Dec 25.","Then every two weeks. December eleventh. December twenty-fifth."),
       B("ink","Last one: JANUARY 8.",["JANUARY"],[A("calendar",0.6,top="JAN",big="8")],"Four payments over six weeks.","And the last one, January eighth."),
       B("yellow","38% plan to SPLIT this season.",["SPLIT"],[A("pie",0.6,frac=0.38,label="38%")],"Of holiday shoppers expect to use pay-later (NerdWallet/Harris Poll).","Thirty-eight percent of holiday shoppers plan to use pay later this year."),
       B("ink","3 deals = 12 PAYMENTS.",["PAYMENTS."],[A("receipt",0.62,rows=(("Deal 1","x4"),("Deal 2","x4"),("Deal 3","x4")),total=("PAYMENTS","12"),title="EXAMPLE")],"Stack three Black Friday deals and the payments stack through the holidays.","Stack three deals, and that's twelve payments landing through the holidays."),
       B("cream","Put all 4 dates in your CALENDAR.",["CALENDAR."],[A("checklist",0.66,rows=("NOV 27","DEC 11","DEC 25","JAN 8"))],"Before you tap buy, not after.","Before you tap buy, put all four dates in your calendar."),
       END("Save this for Black Friday + send it to your deal hunter.","Follow for Part 2: the hotel price that grows at checkout.","Sources: NerdWallet/Harris Poll (via 24/7 Wall St.) · Example prices","Save this for Black Friday, and send it to your deal hunter.","Follow for part two: the hotel price that grows at checkout.")],
 ig="Your Black Friday TV bills you on Christmas 🎄\n\nExample: a $300 TV on pay-in-4 is 4 × $75. Payment 1 lands on Black Friday, Nov 27. Then every two weeks: Dec 11, Dec 25 (Christmas Day) and Jan 8.\n\n38% of holiday shoppers expect to use buy now, pay later this season. Stack three deals and that's 12 payments through the holidays.\n\nThe fix: before you tap buy, put all four dates in your calendar.\n\nWhen does your last holiday payment land? 👇 Send this to your deal hunter.\n\nSources: NerdWallet/Harris Poll survey (via 24/7 Wall St., Nov 2026). Example prices.\n\n#blackfriday #buynowpaylater #budgeting #moneytips #personalfinance",
 tt="Black Friday pay in 4: your 3rd payment lands on Christmas 🎄 When's your last one? 👇 #blackfriday #buynowpaylater #moneytok #budgeting"))

# 7. Wed Nov 25 - hotel fees (Ep 4 bridge)
S.append(dict(n=7, date="2026-11-25", slug="hotel-150-210", file="150 a Night Then Checkout Says 210 - The Hotel Fee Trick",
 hooks=[("surprise","$150 a night. Checkout says $210.","A hundred fifty a night. Checkout says two ten."),
        ("ego","You didn't pick wrong. The fee HID.","You didn't pick wrong. The fee was hidden."),
        ("fear","This $60 only shows up LAST.","This sixty dollars only shows up last."),
        ("urgency","Booking holiday travel? Check the LAST screen.","Booking holiday travel? Check the last screen."),
        ("desire","The rule that forces the REAL price.","There's a rule that forces the real price.")],
 A=H("cream","$150 a night. Checkout says $210.",["$210."],[A("hotel_bell",0.5,0.3,0.52),A("price_tag",0.45,0.73,0.46,delay=0.5,txt="$210")],"Example prices.","A hundred fifty a night. Checkout says two ten.",None),
 B=H("ink","You didn't pick wrong. The fee HID.",["HID."],[A("receipt",0.62,rows=(("Room","$150"),("Resort fee","+$45"),("Service fee","+$15")),total=("TOTAL","$210"),title="EXAMPLE")],"Example prices.","You didn't pick wrong. The fee was hidden."),
 C=H("yellow","This $60 only shows up LAST.",["LAST."],[A("price_tag",0.6,txt="+$60")],"Resort fee + service fee. Example prices.","This sixty dollars only shows up last."),
 body=[B("ink","$150 a night.",["$150"],[A("hotel_bell",0.5,0.3,0.52),A("price_tag",0.45,0.73,0.46,delay=0.4,txt="$150")],"Example prices.","Example: a hotel says a hundred fifty a night."),
       B("cream","Then the FEES.",["FEES."],[A("receipt",0.62,rows=(("Room","$150"),("Resort fee","+$45"),("Service fee","+$15")),total=("TOTAL","$210"),title="EXAMPLE")],"Added after you've already decided.","Then a forty-five dollar resort fee. Then a fifteen dollar service fee."),
       B("red","40% more than you PICKED.",["PICKED."],[A("bars2",0.6,a="$150",b="$210",la="PICKED",lb="PAID",ha=0.71,hb=1.0)],"Example prices.","Two hundred ten. Forty percent more than you picked."),
       B("yellow","The rule: TOTAL up front.",["TOTAL"],[A("gavel",0.6)],"Since May 12, 2025, the FTC fees rule covers hotels and live-event tickets.","Since May twenty twenty-five, a US rule says hotels and event tickets must show the total up front.",7),
       B("ink","But only hotels and TICKETS.",["TICKETS."],[A("ticket",0.6,txt="RULE")],"Other purchases aren't covered by that rule.","But that rule only covers hotels and tickets."),
       B("cream","Compare the LAST screen.",["LAST"],[A("big_button",0.62,txt="FINAL TOTAL")],"Go to the final checkout screen before you compare.","So compare prices on the last screen, never the first."),
       END("Save this before you book your holiday trip.","Follow: the full hidden-fee investigation drops Sunday.","Sources: FTC Rule on Unfair or Deceptive Fees (16 CFR 464) · Example prices","Save this before you book your holiday trip.","Follow. The full hidden fee investigation drops Sunday.")],
 ig="$150 a night. Then checkout says $210 🏨\n\nExample: a $45 resort fee and a $15 service fee, added after you've already decided. That's 40% more than the price you picked.\n\nSince May 12, 2025, a US federal rule says hotels and live-event tickets must show the total price up front. But that rule only covers hotels and tickets.\n\nThe fix: compare prices on the final checkout screen, never the first.\n\nWhat's the worst surprise fee you've paid? 👇 Full hidden-fees investigation on YouTube this Sunday.\n\nSource: FTC Rule on Unfair or Deceptive Fees (16 CFR 464). Example prices.\n\n#hiddenfees #junkfees #resortfees #travelhacks #moneytips",
 tt="$150 hotel, $210 at checkout 🏨 What's the worst surprise fee you've paid? 👇 #hiddenfees #junkfees #resortfees #moneytok"))

SLOTS = {  # ET slot, PT, PHT per new calendar
 "2026-11-19": ("Thu 12:00 PM ET","9:00 AM PT","Fri Nov 20, 1:00 AM PHT","Thu 3:00 PM ET / Fri Nov 20, 4:00 AM PHT","Thu 6:00 PM ET / Fri Nov 20, 7:00 AM PHT"),
 "2026-11-20": ("Fri 10:00 AM ET","7:00 AM PT","Fri Nov 20, 11:00 PM PHT","Fri 3:00 PM ET / Sat Nov 21, 4:00 AM PHT","Fri 6:00 PM ET / Sat Nov 21, 7:00 AM PHT"),
 "2026-11-21": ("Sat 10:00 AM ET","7:00 AM PT","Sat Nov 21, 11:00 PM PHT","Sat 10:00 AM ET / Sat Nov 21, 11:00 PM PHT","Sat 6:00 PM ET / Sun Nov 22, 7:00 AM PHT"),
 "2026-11-22": ("Sun 10:00 AM ET","7:00 AM PT","Sun Nov 22, 11:00 PM PHT","Sun 10:00 AM ET / Sun Nov 22, 11:00 PM PHT","Sun 6:00 PM ET / Mon Nov 23, 7:00 AM PHT"),
 "2026-11-23": ("Mon 12:00 PM ET","9:00 AM PT","Tue Nov 24, 1:00 AM PHT","Mon 3:00 PM ET / Tue Nov 24, 4:00 AM PHT","Mon 6:00 PM ET / Tue Nov 24, 7:00 AM PHT"),
 "2026-11-24": ("Tue 12:00 PM ET","9:00 AM PT","Wed Nov 25, 1:00 AM PHT","Tue 3:00 PM ET / Wed Nov 25, 4:00 AM PHT","Tue 6:00 PM ET / Wed Nov 25, 7:00 AM PHT"),
 "2026-11-25": ("Wed 12:00 PM ET","9:00 AM PT","Thu Nov 26, 1:00 AM PHT","Wed 3:00 PM ET / Thu Nov 26, 4:00 AM PHT","Wed 6:00 PM ET / Thu Nov 26, 7:00 AM PHT"),
}

def clean(b):
    b = copy.deepcopy(b)
    for k in ("say", "tt_say", "tt_end"): b.pop(k, None)
    for a in b.get("art", []):
        ar = a.get("args", {})
        if "color" in ar and isinstance(ar["color"], str): pass
    return b

def cut(st, which):
    hook = st[which]; body = st["body"]
    beats = [hook] + body
    r = dict(date=st["date"], slug=f"w05b-{st['n']}-{st['slug']}-{which.lower()}", beats=[])
    tiktok = which == "C"
    cover = {k: v for k, v in hook.items() if k in ("bg", "head", "hl", "hsize", "art", "sub", "sticker")}
    r["cover"] = copy.deepcopy(cover)
    for b in beats:
        nb = clean(b)
        if tiktok:
            nb["series"] = f"PAY LATER · DAY {st['n']}"
            for a in nb.get("art", []): a["x"] = round(min(a.get("x", 0.5), 0.62) * 0.94, 3); a["s"] = round(a["s"] * 0.9, 3)
            if b.get("end"): nb["end"] = b["tt_end"]
        r["beats"].append(nb)
    if tiktok:
        r["cover"]["series"] = f"PAY LATER · DAY {st['n']}"
        for a in r["cover"]["art"]: a["x"] = round(min(a.get("x", 0.5), 0.62) * 0.94, 3); a["s"] = round(a["s"] * 0.9, 3)
    return r

reels = [cut(s, "A") for s in S]; trials = [cut(s, "B") for s in S]; tts = [cut(s, "C") for s in S]
json.dump(reels, open("reels.json", "w"), indent=1, ensure_ascii=False)
json.dump(trials, open("trials.json", "w"), indent=1, ensure_ascii=False)
json.dump(tts, open("tiktoks.json", "w"), indent=1, ensure_ascii=False)
# Kokoro: one file for the week. ids: story n*100 + 10 hookA, +20 hookB, +30 hookC, +40.. body, +90 IG end, +95 TT end
lines = []
for s in S:
    base = s["n"] * 100
    lines += [dict(id=base + 10, chapter=f"day{s['n']}-hook-a", text=s["A"]["say"]), dict(id=base + 20, chapter=f"day{s['n']}-hook-b", text=s["B"]["say"]), dict(id=base + 30, chapter=f"day{s['n']}-hook-c", text=s["C"]["say"])]
    for i, b in enumerate(s["body"][:-1]): lines.append(dict(id=base + 40 + i * 5 if False else base + 40 + i * 6, chapter=f"day{s['n']}-body", text=b["say"]))
    lines += [dict(id=base + 90, chapter=f"day{s['n']}-end-ig", text=s["body"][-1]["say"]), dict(id=base + 95, chapter=f"day{s['n']}-end-tt", text=s["body"][-1]["tt_say"])]
json.dump(lines, open("thecostnerd-ig-w05b-lines.json", "w"), indent=1, ensure_ascii=False)
meta = [dict(n=s["n"], date=s["date"], slug=s["slug"], file=s["file"], hooks=s["hooks"], ig=s["ig"], tt=s["tt"], slot=SLOTS[s["date"]],
             script=[s["A"]["say"]] + [b["say"] for b in s["body"]]) for s in S]
json.dump(meta, open("meta.json", "w"), indent=1, ensure_ascii=False)
for s in S:
    w = len(re.findall(r"[A-Za-z'-]+", " ".join([s["A"]["say"]] + [b["say"] for b in s["body"]])))
    print(s["n"], s["slug"], w, "words", "| IG caption", len(s["ig"]), "| TT", len(s["tt"]))
print(len(lines), "Kokoro lines")
