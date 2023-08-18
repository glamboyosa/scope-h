import { useQuery } from "@tanstack/react-query";
import { useSearchParams } from "react-router-dom";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

type influencerResponse = {
  data: Array<{
    influencers: string;
    caption_text: string;
    taken_at: string;
    posts: number;
    "post hashtags": number;
    "post mentions": number;
    score: number;
  }> | null;

  status: "processing" | "completed";
};

const r = [
  {
    influencers: "aanorling",
    caption_text:
      "För dig morfar ❤️🕊 tack snälla för hjälpen @onemiletattoo \n\nTack morfar för att du gav oss musiken. Du var en sann musiker ut i fingerspetsarna. Jag har aldrig sett någon som fullkomligt älskade livet genom musik så som du gjorde. Musiken läkte dig och den läker oss. Kommer aldrig sluta höra dina ljuva toner inom mig. Vi ses igen, vår älskade ängel ❤️",
    taken_at: "2023-07-28T11:28:39",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "addidaudi",
    caption_text: "<33333",
    taken_at: "2023-07-28T16:20:41",
    posts: 1,
    "post hashtags": 2,
    "post mentions": 0,
    score: 3,
  },
  {
    influencers: "adelinaadelina",
    caption_text:
      "I said YES 💍🤍 \n\nIt feels so unreal and I have never been happier. Can’t wait to get married with the love of my life.",
    taken_at: "2023-07-30T19:57:15",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "adrianabrunstrom",
    caption_text:
      "Klagar inte på födelsedagsfirande & många blombuketter rikare💐🥹🫶🏼",
    taken_at: "2023-07-30T20:25:15",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "ahintofscandinavia",
    caption_text:
      "Loma oli 🫶🏼 \n\nRakastin siinä kaikkea.\n\nMe niin nautittiin, kaikki. \n\nEi aikaisia aamuja tai herätyskelloon heräämisiä, ei kiirettä. Vähän suunniteltiin, mutta enimmäkseen mentiin fiiliksen mukaan. \n\nTehtiin päiväretkiä niin kauniisiin paikkoihin, syötiin hyvin ja herkuteltiin paljon. \nLöhöiltiin rannalla ja uitiin paljon meressä sekä uima-altaassa. \n\nTähän vielä pakko lainata pojan sanoja, joka jo loman alussa totesi:\n”Äiti, tää on liian ihanaa”\n\nOlen samaa mieltä, loma oli liian ihana ja oon aivan onnellinen, että saatiin viettää lomaa meidän toisessa kotimaassa.\n\nIkävä on, mutta onneksi loma jatkuu ❤️\n\n#vacationmood #vacationislife #lifeisbeautiful",
    taken_at: "2023-07-18T18:36:30",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "almabsvanqvist",
    caption_text:
      "(Samarbete) Magisk kostym från bästa @bubbleroom 💭\n\nJust nu får du hela 10% rabatt på Bubblerooms sortiment, gäller även på andra erbjudanden, använd koden ALMAB 🎉👏🏼\n\n#bubbleroomstyle #dressup #showup #sweden",
    taken_at: "2023-07-17T21:11:42",
    posts: 1,
    "post hashtags": 2,
    "post mentions": 0,
    score: 3,
  },
  {
    influencers: "amandaedvardssson",
    caption_text: "Från en bra kväll på ön🤠🤠",
    taken_at: "2023-07-10T18:10:19",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "amandalantz95",
    caption_text:
      "It was my birthday on Thursday, I thought I would post a post then but unfortunately I didn't have time as I was busy all day and was celebrated by family, the boyfriend and also his family. 🥰 First we were at our house and had a little coffee and I also got some presents and later in the evening we went to eat at a restaurant. It was nice 🌹 \n.\n.\n.\n.\n#belatedbirthday #birthdayfashion #roses #twopieceset #fashionista #fashionable #fashionstyle #fashiongram #fashioninspo #fashiondaily #fashionaddict #chiquelle #mixedwomen #fashionpost #fashionphotography #fashionlover #fashionweek #whatiwore #outfitlook #fashionforward #fashionlove #fashioneditorial #ootd #discoverunder40k #fashionstylist #fashionablestyle #brownskinpoppin #brownskinbeauty \n#rosegarden #georgiaportogallolimited",
    taken_at: "2023-07-17T16:18:21",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "amandarahnboy",
    caption_text: "Tema: favoritpersoner 🧡",
    taken_at: "2023-07-28T13:01:57",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "ameliesjobring",
    caption_text:
      "Mysig kväll med syster @linneasjobring och @oktay.cimen 😍 köpte pinsa bröd från @zeta.nu och la på den ena, mozzarella, tomat, burrata och basilika med salt & peppar och ringlade sedan tryffelolja över. Den andra körde jag mozzarella i botten, löjrom med smetana, gräslök & rödlök😋",
    taken_at: "2023-07-29T19:04:48",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "_andreacontrs",
    caption_text: "Soon ☀️🥹🌻🦋",
    taken_at: "2023-07-30T19:14:51",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "annaamellqvist",
    caption_text:
      "The perfect hideaway 🤍 loved this corner room @esperos.villageblue",
    taken_at: "2023-07-30T21:55:04",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "annaantwan",
    caption_text: "🖤",
    taken_at: "2023-07-30T19:00:59",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
  {
    influencers: "anna.lena.nn",
    caption_text:
      "Det‎ blev‎ otroligt‎ fina‎ fotbollsdagar‎ -‎ endast‎ under‎ en‎ av‎ sex‎ matcher‎ behövde‎ vi‎ paraplyet‎ -‎ annars‎ var‎ det‎ shortsväder‎ hela‎ tiden‎ ☀️‎👌🤩‎ \n⁣\n⁣\n⁣\n⁣\n⁣\n⁣\n⁣\n⁣\n⁣\n⁣\n⁣⁣#umeå‎‎ #visitumeå‎‎ #umeåfotbollsfestival‎‎ #fotbollscup‎‎ #fotboll‎‎ #soccer‎‎ #sweden‎‎ #visitsweden‎‎ #wasaline‎‎ #bluesky‎ #blåhimmel‎ #bluesea‎ #vacation‎ #umeälven‎ #bridge",
    taken_at: "2023-07-30T19:16:12",
    posts: 1,
    "post hashtags": 3,
    "post mentions": 0,
    score: 4,
  },
  {
    influencers: "annamatkovich",
    caption_text: "Sundays ❤️\n\n📸 by @g83.visuals",
    taken_at: "2023-07-30T18:19:27",
    posts: 1,
    "post hashtags": 0,
    "post mentions": 2,
    score: 3,
  },
  {
    influencers: "aqvistemilia",
    caption_text: "Detta 🌅🧡🩷",
    taken_at: "2023-07-30T17:13:45",
    posts: 0,
    "post hashtags": 0,
    "post mentions": 0,
    score: 0,
  },
];
const InfluencerPage = () => {
  const [searchParams] = useSearchParams();

  const task_id = searchParams.get("id");
  const { data, isLoading, error } = useQuery<influencerResponse>({
    queryKey: ["fetchBackground"],
    queryFn: (): Promise<influencerResponse> =>
      fetch(`http://localhost:8000/background-task/${task_id}`).then((res) =>
        res.json()
      ),
    enabled: false,
    refetchInterval: 2000,
  });
  console.log("DATA IS", data);
  console.log(data?.data);
  console.log(Object.keys(r[0]));
  if (error) return <div>Something went wrong</div>;
  if (isLoading && !data) return <img className="mb-8" src="/loading.webp" />;
  return (
    <div>
      <button
        onClick={() => console.log("hey")}
        className="p-4 rounded-md bg-pink-400 font-md hover:bg-pink-300"
      >
        Print 👩🏿‍🎤
      </button>
      <Table>
        <TableCaption className="flex gap-4">
          <div>Bubble room influencers (July 1-31 2023)</div>
          <img src="/bubble(700x100).png" className="w-3/4" />
        </TableCaption>
        <TableHeader>
          <TableRow>
            {Object.keys(r[0]).map((colName) => (
              <TableHead className="w-[100px] text-lg">{colName}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {r.map((row) => (
            <TableRow>
              <TableCell className="font-medium text-base">
                {row.influencers}
              </TableCell>
              <TableCell className="font-medium text-base">
                {row.caption_text}
              </TableCell>
              <TableCell className="font-medium text-base">
                {row.taken_at}
              </TableCell>
              <TableCell className="font-medium text-base">
                {row.posts}
              </TableCell>
              <TableCell className="font-medium text-base">
                {row["post hashtags"]}
              </TableCell>
              <TableCell className="font-medium text-base">
                {row["post mentions"]}
              </TableCell>
              <TableCell className="font-medium text-base">
                {row.score}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default InfluencerPage;
