import React from "react";
import {
  BezierEdge,
  getBezierPath,
  EdgeLabelRenderer,
  useReactFlow,
} from "reactflow";
import CloseIcon from "@mui/icons-material/Close";
import { useStore } from "../store";

const CustomEdge = (props) => {
  // const { setEdges } = useReactFlow();
  const deleteEdge = useStore((state) => state.deleteEdge);

  const {
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    id,
  } = props;
  const [, labelX, lableY] = getBezierPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
  });
  return (
    <>
      <BezierEdge {...props} />;
      <EdgeLabelRenderer>
        <CloseIcon
          fontSize={"small"}
          sx={{
            color: "red",
            position: "absolute",
            transform: `translate(-50%,-50%) translate(${labelX}px,${lableY}px)`,
            cursor: "pointer",
            pointerEvents: "all",
          }}
          onClick={() => {
            // setEdges((prev) => {

            //   return prev.filter((el) => el.id !== id);
            // });
            deleteEdge(id);
          }}
        />
      </EdgeLabelRenderer>
    </>
  );
};

export default CustomEdge;
