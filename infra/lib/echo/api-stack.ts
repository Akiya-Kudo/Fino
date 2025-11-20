import { Construct } from "constructs";
import { BaseInfo, BaseStack } from "../base/base-stack";
import { StackProps } from "aws-cdk-lib";
import { ServiceGroupName } from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";

export class EchoApiStack extends BaseStack {
  constructor(scope: Construct, props?: StackProps) {
    const baseInfo: BaseInfo = {
      serviceGroupName: ServiceGroupName.ECHO,
      systemGroupName: SystemGroup.API,
      serviceBaseName: "Api",
    }
    super(scope, baseInfo, props);
  }
}
