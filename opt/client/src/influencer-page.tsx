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
    refetchInterval: 4000,
  });
  if (error) return <div>Something went wrong</div>;
  if (isLoading && !data) return <img className="mb-8" src="/loading.webp" />;
  return (
    <div>
      <button
        onClick={() => window.print()}
        className="px-4 py-2 rounded-md mt-4 bg-pink-400 font-md hover:bg-pink-300"
      >
        Print 👩🏿‍🎤
      </button>
      <Table>
        <TableCaption className="flex mb-3 items-center">
          <div className="whitespace-nowrap text-sm">(July 1-31 2023)</div>
          <img src="/bubble(700x100).png" className="w-3/4" />
        </TableCaption>
        <TableHeader>
          <TableRow>
            {Object.keys(data!.data![0]).map((colName) => (
              <TableHead
                className={`text-lg p-3 whitespace-nowrap ${
                  colName === "caption_text" ? "w-[200px]" : " w-[1px]"
                }`}
              >
                {colName}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data!.data!.map((row) => (
            <TableRow>
              <TableCell className="font-medium  text-base">
                {row.influencers}
              </TableCell>
              <TableCell className="font-medium w-[300px] text-base">
                {row.caption_text}
              </TableCell>
              <TableCell className="font-medium  text-base">
                {row.taken_at}
              </TableCell>
              <TableCell className="font-medium  text-base">
                {row.posts}
              </TableCell>
              <TableCell className="font-medium  text-base">
                {row["post hashtags"]}
              </TableCell>
              <TableCell className="font-medium  text-base">
                {row["post mentions"]}
              </TableCell>
              <TableCell className="font-medium  text-base">
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
